import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

db = mongo_client["fluxos_database"] # Cria a base de dados "fluxos_database" se ela não existir

collection = db["mawi_collection"] # Cria a coleção "mawi_collection" se ela não existir

collection.drop() # Limpa a coleção