''' instalar pymongo e python-dotenv '''
from dotenv import load_dotenv
import os
import pymongo


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

# Seleciona o banco de dados (será criado se não existir)
db = client.biblioteca

# Envia um ping para confirmar uma conexão bem-sucedida
try:
    client.admin.command('ping')
    print("Ping para sua implantação bem-sucedido. Você se conectou com sucesso ao MongoDB!")
except Exception as e:
    print(e)


ex1 = db.exemplar_ref_livro
liv1 = db.livro_puro
ex2 = db.exemplar_contem_livro
ex3 = db.exemplar_puro
liv3 = db.livro_lista_ref_exemplar
liv4 = db.livro_lista_completo_exemplar

liv1.drop()
ex1.drop()
ex2.drop()
ex3.drop()
liv3.drop()
liv4.drop()

#todas as consultas são "qual a edição dos exemplares de um livro com título Dom Casmurro"
liv1.insert_many([
    {"_id": "0000000001", "titulo": "Dom Casmurro", "ano": 1899},
    {"_id": "0000000002", "titulo": "Memórias Póstumas de Brás Cubas", "ano": 1881},
])

ex1.insert_many([
    {"_id": 1, "livro_fk": "0000000001", "edicao": 1, "bib_fk": "00000123", "secao_fk": "0000000001"},
    {"_id": 2, "livro_fk": "0000000001", "edicao": 1, "bib_fk": "00000123", "secao_fk": "0000000000"},
    {"_id": 3, "livro_fk": "0000000001", "edicao": 2, "bib_fk": "00000456", "secao_fk": "0000000001"},
    {"_id": 4, "livro_fk": "0000000002", "edicao": 1, "bib_fk": "00000123", "secao_fk": "0000000001"}
])

print("Cenário 1")
# id_livro = liv1.find_one({"titulo": "Dom Casmurro"})["_id"]
# exemplares = ex1.find({"livro_fk": id_livro})
# for e in exemplares:
#     print(f'{e["_id"]} - {e["edicao"]}')

pipeline = [
    {"$match": {"titulo": "Dom Casmurro"}},
    {"$lookup": {
        "from": "exemplar_ref_livro",
        "localField": "_id",
        "foreignField": "livro_fk",
        "as": "exemplares"
    }},
    {"$unwind": "$exemplares"},
    {"$project": {"_id": "$exemplares._id", "edicao": "$exemplares.edicao"}}
]
for doc in db.livro_puro.aggregate(pipeline):
    print(doc) 


ex2.insert_many([
    {"_id": 1, "livro": {"_id": "0000000001", "titulo": "Dom Casmurro", "ano": 1899}, "edicao": 1, "bib": {"_id": "00000123"}, "secao": {"_id": ("00000123", "0000000001"), "descricao": "Literatura Nacional"}},
    {"_id": 2, "livro": {"_id": "0000000001", "titulo": "Dom Casmurro", "ano": 1899}, "edicao": 1, "bib": {"_id": "00000123"}, "secao": {"_id": ("00000123", "0000000000"), "descricao": "Estoque"}},
    {"_id": 3, "livro": {"_id": "0000000001", "titulo": "Dom Casmurro", "ano": 1899}, "edicao": 2, "bib": {"_id": "00000456"}, "secao": {"_id": ("00000456", "0000000001"), "descricao": "Literatura Nacional"}},
    {"_id": 4, "livro": {"_id": "0000000002", "titulo": "Memórias Póstumas de Brás Cubas", "ano": 1881}, "edicao": 1, "bib": {"_id": "00000123"}, "secao": {"_id": ("00000123", "0000000001"), "descricao": "Literatura Nacional"}}
])


print('\nCenário 2')
# id_livro = liv1.find_one({"titulo": "Dom Casmurro"})["_id"]
# exemplares = ex2.find({"livro._id": id_livro})
# for e in exemplares:
#     print(f'{e["_id"]} - {e["edicao"]}')
pipeline_cenario2 = [
    {"$match": {"livro.titulo": "Dom Casmurro"}},
    {"$project": {"_id": 1, "edicao": 1}}
]
for doc in ex2.aggregate(pipeline_cenario2):
    print(doc)

liv3.insert_many([
    {"_id": "0000000001", "titulo": "Dom Casmurro", "ano": 1899, "exemplares": [1, 2, 3]},
    {"_id": "0000000002", "titulo": "Memórias Póstumas de Brás Cubas", "ano": 1881, "exemplares": [4]},
])

ex3.insert_many([
    {"_id": 1, "edicao": 1},
    {"_id": 2, "edicao": 1},
    {"_id": 3, "edicao": 2},
    {"_id": 4, "edicao": 1}
])

print('\nCenário 3')
pipeline_cenario3 = [
    {"$match": {"titulo": "Dom Casmurro"}},   
    {"$unwind": "$exemplares"},                 
    {"$lookup": {
        "from": "exemplar_puro",               
        "localField": "exemplares",            
        "foreignField": "_id",
        "as": "exemplar_doc"
    }},
    {"$unwind": "$exemplar_doc"},
    {"$project": {"_id": "$exemplares", "edicao": "$exemplar_doc.edicao"}}
]
for doc in liv3.aggregate(pipeline_cenario3):
    print(doc)


liv4.insert_many([
    {"_id": "0000000001", "titulo": "Dom Casmurro", "ano": 1899, "exemplares": [{"_id": 1, "edicao": 1},
                                                                                {"_id": 2, "edicao": 1},
                                                                                {"_id": 3, "edicao": 2}]},
    {"_id": "0000000002", "titulo": "Memórias Póstumas de Brás Cubas", "ano": 1881, "exemplares": [{"_id": 4, "edicao": 1}]},
])

print('\nCenário 4')
# livro = liv4.find_one({"titulo": "Dom Casmurro"})
# for e in livro["exemplares"]:
#     print(f'{e["_id"]} - {e["edicao"]}')
pipeline_cenario4 = [
    {"$match": {"titulo": "Dom Casmurro"}},   
    {"$unwind": "$exemplares"},
    {"$project": {"_id": "$exemplares._id", "edicao": "$exemplares.edicao"}}
]
for doc in liv4.aggregate(pipeline_cenario4):
    print(doc)

client.close()