import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

# --- Conexão ---
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["biblioteca"]

def setup_indexes():
    """Cria índices importantes para consultas."""
    db.socio.create_index([("cpf", ASCENDING)], unique=True)
    db.emprestimo.create_index([("cpf_socio", ASCENDING)])
    db.emprestimo.create_index([("devolvido", ASCENDING)])
    print("Índices criados.")


# Cenário 1 - documento referenciando apenas um documento,

def scenario_1_reference_single():
    """Emprestimo referencia socio por cpf."""

    socios = [
        ("11122233344", "Ana", "0000001"),
        ("22233344455", "Bruno", "0000002"),
        ("43344455566", "Carla", "0000003"),
        ("44455566677", "Diego", "0000004"),
        ("55566677788", "Elisa", "0000005"),
    ]
    for cpf, nome, cartao in socios:
        db.socio.insert_one({"cpf": cpf, "nome": nome, "cartao": cartao})

    emprestimos = [
        ("11122233344", datetime(2025, 8, 1), datetime(2025, 8, 15), False),
        ("22233344455", datetime(2025, 7, 25), datetime(2025, 8, 5), True),
        ("33344455566", datetime(2025, 8, 3), datetime(2025, 8, 17), False),
        ("44455566677", datetime(2025, 7, 20), datetime(2025, 7, 30), True),
        ("55566677788", datetime(2025, 8, 5), datetime(2025, 8, 20), False),
    ]
    for cpf_socio, data, prazo, dev in emprestimos:
        db.emprestimo.insert_one({
            "cpf_socio": cpf_socio,
            "data": data,
            "prazo": prazo,
            "devolvido": dev
        })

    print("\n[Scenario 1] Sócios e Empréstimos de Referência Única criados")
    pipeline = [
        {"$lookup": {
            "from": "socio",
            "localField": "cpf_socio",
            "foreignField": "cpf",
            "as": "socio"
        }},
        {"$unwind": "$socio"},
        {"$project": {
            "_id": 0,
            "cpf_socio": 1,
            "nome": "$socio.nome",
            "devolvido": 1
        }}
    ]
    result = list(db.emprestimo.aggregate(pipeline))
    for r in result:
        print(f"Nome: {r['nome']}, CPF: {r['cpf_socio']}, Devolvido: {r['devolvido']}")


# Cenário 2 - documento embutindo apenas um documento

def scenario_2_embed_single():
    socio_doc = {
        "cpf": "22233344456",
        "nome": "Carlos",
        "cartao": "0000006"
    }
    db.socio.insert_one(socio_doc)

    db.emprestimo.insert_one({
        "socio": socio_doc,
        "data": datetime(2025, 8, 2),
        "prazo": datetime(2025, 8, 16),
        "devolvido": False
    })

    print("\n[Scenario 2] Empréstimo criado com sócio embutido")
    result = list(db.emprestimo.find(
        {"socio.cpf": socio_doc["cpf"]},
        {"_id": 0, "socio": 1, "devolvido": 1}
    ))
    for r in result:
        print(f"Nome: {r['socio']['nome']}, CPF: {r['socio']['cpf']}, Devolvido: {r['devolvido']}")


# Cenário 3 - documento com um array de referências para documentos

def scenario_3_array_of_references():
    socio_cpf = "43344455566"
    db.socio.replace_one({"cpf": socio_cpf}, {
        "cpf": socio_cpf,
        "nome": "Victor",
        "cartao": "0000007"
    }, upsert=True)

    e1 = db.emprestimo.insert_one({
        "data": datetime(2025, 8, 3),
        "prazo": datetime(2025, 8, 17),
        "devolvido": False
    }).inserted_id
    e2 = db.emprestimo.insert_one({
        "data": datetime(2025, 8, 4),
        "prazo": datetime(2025, 8, 18),
        "devolvido": True
    }).inserted_id

    db.socio.update_one({"cpf": socio_cpf}, {"$set": {"emprestimos_refs": [e1, e2]}})

    print("\n[Scenario 3] Sócio com array de referências criado")
    pipeline = [
        {"$match": {"cpf": socio_cpf}},
        {"$lookup": {
            "from": "emprestimo",
            "localField": "emprestimos_refs",
            "foreignField": "_id",
            "as": "emprestimos"
        }},
        {"$unwind": "$emprestimos"},
        {"$project": {
            "_id": 0,
            "cpf": 1,
            "nome": 1,
            "devolvido": "$emprestimos.devolvido"
        }}
    ]
    result = list(db.socio.aggregate(pipeline))
    for r in result:
        print(f"Nome: {r['nome']}, CPF: {r['cpf']}, Devolvido: {r['devolvido']}")


# Cenário 4 - documento embutindo vários documentos

def scenario_4_embed_many():
    socio_cpf = "54455566677"
    db.socio.replace_one({"cpf": socio_cpf}, {
        "cpf": socio_cpf,
        "nome": "Ingrid",
        "cartao": "0000008",
        "emprestimos": [
            {"id": 10, "data": datetime(2025, 8, 5), "prazo": datetime(2025, 8, 19), "devolvido": False},
            {"id": 11, "data": datetime(2025, 8, 6), "prazo": datetime(2025, 8, 20), "devolvido": True}
        ]
    }, upsert=True)

    print("\n[Scenario 4] Sócio com empréstimos embutidos criado")
    socio = db.socio.find_one({"cpf": socio_cpf}, {"_id": 0})
    for emp in socio.get("emprestimos", []):
        print(f"Nome: {socio['nome']}, CPF: {socio['cpf']}, Devolvido: {emp['devolvido']}")

def run(clean=True):
    if clean:
        db.socio.delete_many({})
        db.emprestimo.delete_many({})
        print("Coleções limpas")

    setup_indexes()
    scenario_1_reference_single()
    scenario_2_embed_single()
    scenario_3_array_of_references()
    scenario_4_embed_many()

if __name__ == "__main__":
    run()
