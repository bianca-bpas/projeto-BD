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

""" # Exemplo de como usar o db:
colecao = db.minha_colecao
colecao.insert_one({"nome": "teste"})

if colecao.find_one({"nome": "teste"}):
    print("Documento inserido com sucesso!") 

client.close()
"""
