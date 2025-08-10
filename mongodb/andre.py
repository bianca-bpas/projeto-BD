import pymongo
import os

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
from pymongo.errors import DuplicateKeyError

db = client["andre"]


collections = db.list_collection_names()
for c in collections:
    db.drop_collection(c)

# foi adicionada a sigla pra fins de demonstração,
# e para replicar a realidae, evitando a digitação do nome da biblioteca

bibliotecas = [("Biblioteca de Ciencias Exatas", "Av D005", "BCC"),
                ("Biblioteca de Ciencias Inexatas", "Rua Dom Bosco, Boa Vista", "BCI"),
                ("Biblioteca dos Nunca-Impressos", "Travessa Araripina, Candeias", "BNI")]

bibliotecadocs = [{"nome": n, "local": a, "sigla": c} for n,a,c in bibliotecas]

bccsec = [("Filosofia America de Liberdade de Software", "FAL"), ("Análise", "ANL")]
bcisec = [("Filosofia Alema", "FAL")]
bcni = []

def cen1():
    t = db["bibliotecas1"]
    #ids nao serao usados para complicar
    ids = t.insert_many(bibliotecadocs).inserted_ids
    
    # impede seções duplicadas e estabelece identificação unica por (biblioteca, sigla)
    # opcional, apenas para replicar as garantias do projeto físico original
    db["secoes1"].create_index([("biblioteca_id", 1), ("sigla", 1)], unique=True)

    for sigla, secoes in [
        ("BCC", bccsec),
        ("BCI", bcisec),
        ("BNI", bcni)]:

        bib_id = t.find_one({"sigla": sigla})["_id"] #type: ignore

        #AQUI
        objs = [{"nome": n, "sigla": s, "biblioteca_id": bib_id } for n, s in secoes]
        try:
            if objs:
                db["secoes1"].insert_many(objs)
        except DuplicateKeyError as e:
            print(f"Duplicate key error: {e}")


def cen2():
    t = db["bibliotecas2"]
    ids = t.insert_many(bibliotecadocs)

    for sigla, secoes in [
        ("BCC", bccsec),
        ("BCI", bcisec),
        ("BNI", bcni)]:

        bib:dict = t.find_one({"sigla": sigla}) #type: ignore
        bib.pop("_id", None)

        if secoes:
            db["secoes2"].insert_many(
            [{"nome": n, "sigla": s, "biblioteca": bib} for n, s in secoes]
        )

def cen3():
    #biblioteca com array de referencias pra secoes
    t = db["bibliotecas3"]

    for bib, secoes in [
        (bibliotecadocs[0],bccsec),
        (bibliotecadocs[1], bcisec),
        (bibliotecadocs[2], bcni)]:

        if secoes:
            secids = db["secoes3"].insert_many(
                [{"nome": n, "sigla": s} for n, s in secoes]
            ).inserted_ids
        else: secids = []

        bib = bib.copy()
        bib["secoes"] = list(secids)
        t.insert_one(bib)


def cen4():
    #biblioteca com array de secoes embutidas
    #correto
    t = db["bibliotecas4"]
    for bib, secoes in [
        (bibliotecadocs[0],bccsec),
        (bibliotecadocs[1], bcisec),
        (bibliotecadocs[2], bcni)]:

        bib = bib.copy()
        bib["secoes"] = [{"nome": n, "sigla": s} for n, s in secoes]
        t.insert_one(bib)


import json

def mostra_dados():
    cen_collections = {
        "cen1": ["bibliotecas1", "secoes1"],
        "cen2": ["bibliotecas2", "secoes2"],
        "cen3": ["bibliotecas3", "secoes3"],
        "cen4": ["bibliotecas4"],
    }

    for cen, colls in cen_collections.items():
        print(f"\n=== {cen} ===")
        for coll in colls:
            docs = list(db[coll].find())
            print(f"\nColeção '{coll}' ({len(docs)} docs):")
            # json.dumps transforma BSON para JSON indentado, convertendo ObjectId em strings
            print(json.dumps(docs, default=str, indent=2, ensure_ascii=False))

cen1()
cen2()
cen3()
cen4()

#mostra_dados()

def consulta1_simples(sigla="BCC"):
    bib = db["bibliotecas1"].find_one({"sigla": sigla})
    if not bib:
        return f"{sigla} Not found!"

    secs = db["secoes1"].find({"biblioteca_id": bib["_id"]})
    return [bib['nome'], [s['nome'] for s in secs]]


def consulta1_pipeline(sigla="BCC"):
    pipeline = [
        {"$match": {"sigla": sigla}}, 
        {"$lookup": {
                "from": "secoes1", 
                "localField": "_id",                
                "foreignField": "biblioteca_id",  
                "as": "secoes_docs"                 
            }
        },
        { "$project": {
                "_id": 0,
                "nome_biblioteca": "$nome",
                "secoes": {
                    "$map": {                      
                        "input": "$secoes_docs",
                        "as": "sec",
                        "in": "$$sec.nome"
                    }
                }
            }
        }
    ]
    r = list(db["bibliotecas1"].aggregate(pipeline))
    return r


def consulta2_pipeline(sigla="BCC"):
    pip = [
        {"$match": {"biblioteca.sigla": sigla}},
        {"$group": {
            "_id": "$biblioteca.nome",
            "secoes": {"$push": "$nome"} #faz array de nome
            }
        },
        {"$project": {
            "_id": 0,
            "biblioteca": "$_id",
            "secoes": 1
        }}]
    return list(db["secoes2"].aggregate(pip))


def consulta3(sigla="BCC"):
    secids = db["bibliotecas3"].find_one({"sigla": sigla})["secoes"] #type:ignore
    secoes = list(db["secoes3"].find({"_id": {"$in": secids}}))
    return [sigla, [s["nome"] for s in secoes]] #so retorna uma

def consulta4(sigla="BCI"):
    bib:dict = db["bibliotecas4"].find_one({"sigla": sigla}) #type:ignore
    return bib["nome"], [s['nome'] for s in bib["secoes"]]
print(consulta4())
