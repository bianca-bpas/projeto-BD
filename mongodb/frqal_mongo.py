import os
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

print("Conexão estabelecida com o banco de dados 'biblioteca'." + "\n")

# Cenário 1 : um documento referenciando apenas um documento
secao_ref_doc = db.colecao_ref_doc    
exemplar_ref_doc = db.exemplar_ref_doc  
secao_ref_doc.drop()
exemplar_ref_doc.drop()

sessao = (
    { "_id": 'A1', "Descrição": "Literatura Infanto-Juvenil" },
    { "_id": 'A2', "Descrição": "Clássicos Brasileiros" },
    { "_id": 'A3', "Descrição": "True Crime" },
)

secao_ref_doc.insert_many([{"_id": c["_id"], "Descrição": c["Descrição"]} for c in sessao])

exemplar = (
    { "_COD": "978-3-16-148410-0", "FK_COD": 'A1', "edicao": "1" },
    { "_COD": "978-3-16-148410-1", "FK_COD": 'A1', "edicao": "2" },
    { "_COD": "978-3-16-148410-2", "FK_COD": 'A1', "edicao": "1" },
    { "_COD": "978-3-16-148410-5", "FK_COD": 'A2', "edicao": "1" },
    { "_COD": "978-3-16-148410-6", "FK_COD": 'A2', "edicao": "1" },
    { "_COD": "978-3-16-148410-7", "FK_COD": 'A2', "edicao": "2" },
)

exemplar_ref_doc.insert_many([{"_COD": b["_COD"], "FK_COD": b["FK_COD"], "edicao": b["edicao"]} for b in exemplar])

# Consulta - buscar exemplares de 'Clássicos Brasileiros'
res1 = secao_ref_doc.aggregate([ #from
    {
        "$lookup": { #join
            "from": "exemplar_ref_doc",  
            "localField": "_id",
            "foreignField": "FK_COD",
            "as": "exemplares"
        }
    },
    {"$match": {"Descrição": "Clássicos Brasileiros"}}, #filter/where
    {"$project": {"exemplares": 1, "_id": 0}} #select
])

print("Cenário 1 : um documento referenciando apenas um documento")
print("Exemplares na seção 'Clássicos Brasileiros'")
for r in res1:
    for i, exemplar in enumerate(r["exemplares"]):
        print(f"Exemplar {i+1}: Código = {exemplar['_COD']}, Edição = {exemplar['edicao']}")

print("\n"*2)

# Cenário 2 :  um documento embutindo apenas um documento
secao_emb_doc = db.secao_emb_doc
secao_emb_doc.drop()

# Documentos com exemplar embutido único
sessao_emb = [
    {
        "_id": "A1",
        "Descrição": "Literatura Infanto-Juvenil",
        "exemplar": {
            "_COD": "978-3-16-148410-0",
            "edicao": "1"
        }
    },
]

secao_emb_doc.insert_many(sessao_emb)
res2 = secao_emb_doc.find({"Descrição": "Literatura Infanto-Juvenil"})

print("Cenário 2 :  um documento embutindo apenas um documento")
print("Exemplares na seção 'Literatura Infanto-Juvenil'")
for doc in res2:
    print(f"Seção: {doc['Descrição']}")
    print(f"Exemplar embutido: Código = {doc['exemplar']['_COD']}, Edição = {doc['exemplar']['edicao']}")

print("\n"*2)


# Cenário 3 : um documento com um array de referências para documentos
secao_ref_doc = db.secao_ref_doc
exemplar_ref_doc = db.exemplar_ref_doc

secao_ref_doc.drop()
exemplar_ref_doc.drop()

# Inserir exemplares
exemplares = [
    {"_COD": "978-3-16-148410-5", "edicao": "1"},
    {"_COD": "978-3-16-148410-6", "edicao": "1"},
    {"_COD": "978-3-16-148410-7", "edicao": "2"},
]
exemplar_ref_doc.insert_many(exemplares)

secoes = [
    {
        "_id": "A2",
        "Descrição": "Clássicos Brasileiros",
        "exemplares": ["978-3-16-148410-5", "978-3-16-148410-6", "978-3-16-148410-7"]
    }
]

secao_ref_doc.insert_many(secoes)

# Consulta com $lookup usando array de referências
res = secao_ref_doc.aggregate([
    {
        "$lookup": {
            "from": "exemplar_ref_doc",
        "localField": "exemplares",   
            "foreignField": "_COD",
            "as": "detalhes_exemplares"
        }
    },
    {"$match": {"Descrição": "Clássicos Brasileiros"}}
])

print("Cenário 3 : um documento com um array de referências para documentos")
for doc in res:
    print(f"Seção: {doc['Descrição']}")
    for exemplar in doc["detalhes_exemplares"]:
        print(f"  Código: {exemplar['_COD']}, Edição: {exemplar['edicao']}")
print("\n"*2)

# Cenário 4 : um documento com um array de documentos embutidos

secao_emb_varios = db.secao_emb_varios
secao_emb_varios.drop()

sessao_emb_varios = [
    {
        "_id": "A2",
        "Descrição": "Clássicos Brasileiros",
        "exemplares": [
            {"_COD": "978-3-16-148410-5", "edicao": "1"},
            {"_COD": "978-3-16-148410-6", "edicao": "1"},
            {"_COD": "978-3-16-148410-7", "edicao": "2"},
        ]
    }
]

secao_emb_varios.insert_many(sessao_emb_varios)

# Consulta simples para pegar os exemplares embutidos
res = secao_emb_varios.find(
    {"Descrição": "Clássicos Brasileiros"},
    {"exemplares": {"$elemMatch": {"edicao": "2"}}, "Descrição": 1, "_id": 0}
)

print("\nCenário 4 : um documento com um array de documentos embutidos")
print("Exemplares na seção 'Clássicos Brasileiros, sendo a segunda edição'")
for doc in res:
    print(f"Seção: {doc['Descrição']}")
    for exemplar in doc["exemplares"]:
        print(f"  Código: {exemplar['_COD']}, Edição: {exemplar['edicao']}")

