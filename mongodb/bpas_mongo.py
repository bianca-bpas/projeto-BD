import os
from datetime import datetime
from dotenv import load_dotenv
import pymongo

# --- Conexão ---
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

db = client.biblioteca

# Ping para confirmar a conexão
try:
    client.admin.command('ping')
    print("Ping para sua implantação bem-sucedido. Você se conectou com sucesso ao MongoDB!")
except Exception as e:
    print(e)

# Coleções por cenário
socio_doc_ref_doc = db.socio_doc_ref_doc
emprestimo_doc_ref_doc = db.emprestimo_doc_ref_doc
socio_doc_embbed_doc = db.socio_doc_embbed_doc
emprestimo_doc_embbed_doc = db.emprestimo_doc_embbed_doc
socio_doc_array_ref_doc = db.socio_doc_array_ref_doc
emprestimo_doc_array_ref_doc = db.emprestimo_doc_array_ref_doc
socio_doc_embbed_mult_docs = db.socio_doc_embbed_mult_docs

# Limpeza de todas as coleções antes de iniciar
for col in [
    socio_doc_ref_doc, emprestimo_doc_ref_doc,
    socio_doc_embbed_doc, emprestimo_doc_embbed_doc,
    socio_doc_array_ref_doc, emprestimo_doc_array_ref_doc,
    socio_doc_embbed_mult_docs
]:
    col.drop()

# Índices por cenário
socio_doc_ref_doc.create_index([("cpf", pymongo.ASCENDING)], unique=True)
emprestimo_doc_ref_doc.create_index([("cpf_socio", pymongo.ASCENDING)])
emprestimo_doc_ref_doc.create_index([("devolvido", pymongo.ASCENDING)])

socio_doc_embbed_doc.create_index([("cpf", pymongo.ASCENDING)], unique=True)
emprestimo_doc_embbed_doc.create_index([("socio.cpf", pymongo.ASCENDING)])

socio_doc_array_ref_doc.create_index([("cpf", pymongo.ASCENDING)], unique=True)
emprestimo_doc_array_ref_doc.create_index([("devolvido", pymongo.ASCENDING)])

socio_doc_embbed_mult_docs.create_index([("cpf", pymongo.ASCENDING)], unique=True)
print("Índices criados.")

# Consulta: Nome e CPF dos sócios de todos os empréstimos não devolvidos

# Cenário 1 - documento referenciando apenas um documento
# Empréstimo referencia Sócio pelo campo cpf_socio
print("Cenário 1")
socios = [
    ("11122233344", "Ana", "0000001"),
    ("22233344455", "Bruno", "0000002"),
    ("43344455566", "Carla", "0000003"),
    ("44455566677", "Diego", "0000004"),
    ("55566677788", "Elisa", "0000005"),
]
socio_doc_ref_doc.insert_many([{"cpf": cpf, "nome": nome, "cartao": cartao} for cpf, nome, cartao in socios])

emprestimos = [
    ("11122233344", datetime(2025, 8, 1), datetime(2025, 8, 15), False),
    ("22233344455", datetime(2025, 7, 25), datetime(2025, 8, 5), True),
    ("33344455566", datetime(2025, 8, 3), datetime(2025, 8, 17), False),
    ("44455566677", datetime(2025, 7, 20), datetime(2025, 7, 30), True),
    ("55566677788", datetime(2025, 8, 5), datetime(2025, 8, 20), False),
]
emprestimo_doc_ref_doc.insert_many([
    {"cpf_socio": cpf_socio, "data": data, "prazo": prazo, "devolvido": dev}
    for cpf_socio, data, prazo, dev in emprestimos
])

# Consulta é feita com um 'join' (lookup)
pipeline_1 = [
    {"$match": {"devolvido": False}},
    {"$lookup": {
        "from": "socio_doc_ref_doc",
        "localField": "cpf_socio",
        "foreignField": "cpf",
        "as": "socio"
    }},
    {"$unwind": "$socio"},
    {"$project": {"_id": 0, "cpf_socio": 1, "nome": "$socio.nome", "devolvido": 1}}
]
for r in emprestimo_doc_ref_doc.aggregate(pipeline_1):
    print(f"Nome: {r['nome']}, CPF: {r['cpf_socio']}, Devolvido: {r['devolvido']}")

''' equivalente SQL
SELECT
    e.cpf_socio,
    s.nome,
    e.devolvido
FROM emprestimo e
INNER JOIN socio s
    ON e.cpf_socio = s.cpf
WHERE e.devolvido = False
'''

# Cenário 2 - documento embutindo apenas um documento
print("\nCenário 2")
socio_doc = {"cpf": "22233344456", "nome": "Carlos", "cartao": "0000006"}
socio_doc_embbed_doc.insert_one(socio_doc)
emprestimo_doc_embbed_doc.insert_one({
    "socio": socio_doc,
    "data": datetime(2025, 8, 2),
    "prazo": datetime(2025, 8, 16),
    "devolvido": False
})
for r in emprestimo_doc_embbed_doc.find(
    {"devolvido": False},
    {"_id": 0, "socio": 1, "devolvido": 1}
):
    print(f"Nome: {r['socio']['nome']}, CPF: {r['socio']['cpf']}, Devolvido: {r['devolvido']}")

''' equivalente SQL
SELECT
    e.nome,
    e.cpf,
    e.devolvido
FROM emprestimo e
WHERE e.devolvido = False
'''

# Cenário 3 - documento com um array de referências para documentos
print("\nCenário 3")
socio_cpf = "43344455566"
socio_doc_array_ref_doc.replace_one({"cpf": socio_cpf}, {
    "cpf": socio_cpf,
    "nome": "Victor",
    "cartao": "0000007"
}, upsert=True)

e1 = emprestimo_doc_array_ref_doc.insert_one({
    "data": datetime(2025, 8, 3),
    "prazo": datetime(2025, 8, 17),
    "devolvido": False
}).inserted_id
e2 = emprestimo_doc_array_ref_doc.insert_one({
    "data": datetime(2025, 8, 4),
    "prazo": datetime(2025, 8, 18),
    "devolvido": True
}).inserted_id

socio_doc_array_ref_doc.update_one({"cpf": socio_cpf}, {"$set": {"emprestimos_refs": [e1, e2]}})

pipeline_3 = [
    {"$lookup": {
        "from": "emprestimo_doc_array_ref_doc",
        "let": {"refs": "$emprestimos_refs"},
        "pipeline": [
            {"$match": {
                "$expr": {
                    "$and": [
                        {"$in": ["$_id", "$$refs"]},
                        {"$eq": ["$devolvido", False]}
                    ]
                }
            }}
        ],
        "as": "emprestimos"
    }},
    {"$unwind": "$emprestimos"},
    {"$project": {"_id": 0, "cpf": 1, "nome": 1, "devolvido": "$emprestimos.devolvido"}}
]

for r in socio_doc_array_ref_doc.aggregate(pipeline_3):
    print(f"Nome: {r['nome']}, CPF: {r['cpf']}, Devolvido: {r['devolvido']}")

''' equivalente SQL
SELECT
    s.nome,
    s.cpf,
    e.devolvido
FROM socio s
INNER JOIN emprestimo e
    ON e.id IN (s.emprestimos_refs)
WHERE e.devolvido = False
'''

# Cenário 4 - documento embutindo vários documentos
print("\nCenário 4")
socio_cpf = "54455566677"
socio_doc_embbed_mult_docs.replace_one({"cpf": socio_cpf}, {
    "cpf": socio_cpf,
    "nome": "Ingrid",
    "cartao": "0000008",
    "emprestimos": [
        {"id": 10, "data": datetime(2025, 8, 5), "prazo": datetime(2025, 8, 19), "devolvido": False},
        {"id": 11, "data": datetime(2025, 8, 6), "prazo": datetime(2025, 8, 20), "devolvido": True}
    ]
}, upsert=True)

pipeline = [
    {"$unwind": "$emprestimos"},
    {"$match": {"emprestimos.devolvido": False}},
    {"$project": {"_id": 0, "nome": 1, "cpf": 1, "devolvido": "$emprestimos.devolvido"}}
]

for r in socio_doc_embbed_mult_docs.aggregate(pipeline):
    print(f"Nome: {r['nome']}, CPF: {r['cpf']}, Devolvido: {r['devolvido']}")

''' equivalente SQL
SELECT
    s.nome,
    s.cpf,
    e.devolvido
FROM socio s
INNER JOIN emprestimo e
    ON s.cpf = e.socio_cpf
WHERE e.devolvido = False
'''

client.close()
