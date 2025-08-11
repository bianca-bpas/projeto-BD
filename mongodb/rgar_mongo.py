from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

db = client.biblioteca

db.exemplar1.drop()
db.emprestimo1.drop()
db.emprestimo2.drop()
db.exemplar3.drop()
db.exemplar4.drop()

try:
    client.admin.command('ping')
    print("Ping para sua implantação bem-sucedido. Você se conectou com sucesso ao MongoDB!")
except Exception as e:
    print(e)

#consulta: id dos emprestimos do livro com ISBN '1111111111111'

db.exemplar1.insert_many([ 
    {"_id": 21, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001"},
    {"_id": 20, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001"},
    {"_id": 11, "ISBN": "2111111111111", "id_biblioteca": "0000000123", "codigo_secao": "0000000003"}
])
db.emprestimo1.insert_many([
    {"_id": 9,  "cpf_socio": "55566677888", "data": "2024-02-02", "prazo": "2024-02-17", "codigo_exemplar": 11, "devolvido": 1},
    {"_id": 10, "cpf_socio": "55566677888", "data": "2024-06-30", "prazo": "2024-07-14", "codigo_exemplar": 20, "devolvido": 0},
    {"_id": 11, "cpf_socio": "71400289223", "data": "2024-05-25", "prazo": "2024-06-10", "codigo_exemplar": 21, "devolvido": 1},
    {"_id": 12, "cpf_socio": "71400289223", "data": "2024-06-10", "prazo": "2024-06-25", "codigo_exemplar": 21, "devolvido": 1}
    
])

print("Cenário 1")
ids_exemplares = [doc["_id"] for doc in db.exemplar1.find(
    {"ISBN": "1111111111111"}
)]
for emp in db.emprestimo1.find({"codigo_exemplar": {"$in": ids_exemplares}}):
    print(emp["_id"])

pipeline1 = [
    {"$match": {"ISBN": "1111111111111"}},
    {"$lookup": {
        "from": "emprestimo1",
        "localField": "_id",
        "foreignField": "codigo_exemplar",
        "as": "emprestimos"
    }},
    {"$unwind": "$emprestimos"},
    {"$project": {"_id": "$emprestimos._id"}}
]

for doc in db.exemplar1.aggregate(pipeline1):
    print(doc["_id"])

db.emprestimo2.insert_many([
    {"_id": 9,  "cpf_socio": "55566677888", "data": "2024-02-02", "prazo": "2024-02-17",
     "exemplar": {"_id": 11, "ISBN": "2111111111111", "id_biblioteca": "0000000123", "codigo_secao": "0000000003"},
     "devolvido": 1},
    {"_id": 10, "cpf_socio": "55566677888", "data": "2024-06-30", "prazo": "2024-07-14",
     "exemplar": {"_id": 20, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001"},
     "devolvido": 0},
    {"_id": 11, "cpf_socio": "71400289223", "data": "2024-05-25", "prazo": "2024-06-10",
     "exemplar": {"_id": 21, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001"},
     "devolvido": 1},
    {"_id": 12, "cpf_socio": "71400289223", "data": "2024-06-10", "prazo": "2024-06-25",
     "exemplar": {"_id": 21, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001"},
     "devolvido": 1}
    
])

print("\nCenário 2")
pipeline2 = [
    {"$match": {"exemplar.ISBN": "1111111111111"}},
    {"$project": {"_id": 1}}
]

for doc in db.emprestimo2.aggregate(pipeline2):
    print(doc["_id"])


db.exemplar3.insert_many([ 
    {"_id": 21, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001","emprestimos": [11, 12]},
    {"_id": 20, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001","emprestimos": [10]},
    {"_id": 11, "ISBN": "2111111111111", "id_biblioteca": "0000000123", "codigo_secao": "0000000003", "emprestimos": [9]}
])

print("\nCenário 3")

for ex in db.exemplar3.find({"ISBN": "1111111111111"}, {"emprestimos": 1, "_id": 0}):
    for id_emp in ex["emprestimos"]:
        print(id_emp)

pipeline3 = [
    {"$match": {"ISBN": "1111111111111"}},
    {"$unwind": "$emprestimos"},
    {"$project": {"_id": "$emprestimos"}}
]

for doc in db.exemplar3.aggregate(pipeline3):
    print(doc["_id"])

db.exemplar4.insert_many([ 
    {"_id": 21, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001","emprestimos": [
        {"_id": 10, "cpf_socio": "55566677888", "data": "2024-06-30", "prazo": "2024-07-14", "codigo_exemplar": 20, "devolvido": 0},
        {"_id": 11, "cpf_socio": "71400289223", "data": "2024-05-25", "prazo": "2024-06-10", "codigo_exemplar": 21, "devolvido": 1}
    ]},
    {"_id": 20, "ISBN": "1111111111111", "id_biblioteca": "4560010000", "codigo_secao": "0000000001","emprestimos": [
        {"_id": 12, "cpf_socio": "71400289223", "data": "2024-06-10", "prazo": "2024-06-25", "codigo_exemplar": 21, "devolvido": 1}
    ]},
    {"_id": 11, "ISBN": "2111111111111", "id_biblioteca": "0000000123", "codigo_secao": "0000000003", "emprestimos": [
        {"_id": 9,  "cpf_socio": "55566677888", "data": "2024-02-02", "prazo": "2024-02-17", "codigo_exemplar": 11, "devolvido": 1}
    ]}
])

print("\nCenário 4")
pipeline4 = [
    {"$match": {"ISBN": "1111111111111"}},
    {"$unwind": "$emprestimos"},
    {"$project": {"_id": "$emprestimos._id"}}
]

for doc in db.exemplar4.aggregate(pipeline4):
    print(doc["_id"])