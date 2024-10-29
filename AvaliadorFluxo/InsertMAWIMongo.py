import pymongo
import time
from FluxoFile import FluxoFile


file_name = "AvaliadorFluxo\Saida\FluxosOrdenados-MAWI.txt"

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

db = mongo_client["fluxos_database"] # Cria a base de dados "fluxos_database" se ela não existir

collection = db["mawi_collection"] # Cria a coleção "mawi_collection" se ela não existir

# Pega o tempo inicial
start_time = time.time()

# Printa o início do processo
print("Inserindo os fluxos no banco de dados...")
print("Arquivo:", file_name)
print("Base de dados:", db.name)
print("Coleção:", collection.name)
print("Horário:", time.strftime("%H:%M:%S", time.localtime(start_time)))

batch_size = 10000  # Ajuste o tamanho do lote de acordo com a memória disponível
batch = []

with open(file_name, "r") as file:
    for line in file:
        # 23.36.44.166:443 <-> 163.33.141.15:52079          0 0 bytes      36136 2385012 bytes      36136 2385012 bytes 0,000000  71,916941
        fluxo = FluxoFile(line)

        if fluxo.ipv6:
            continue

        # Cria um dicionário com os dados do fluxo
        fluxo_dict = fluxo.to_dict()

        # Adiciona o dicionário ao lote
        batch.append(fluxo_dict)

        # Insere o dicionário na coleção
        if len(batch) == batch_size:
            collection.insert_many(batch)
            batch = []

    # Insere o restante dos fluxos
    if batch:
        collection.insert_many(batch)

# Pega o tempo final
final_time = time.time()

# Calcula o tempo de execução
execution_time = final_time - start_time

print(f"Tempo de execução: {execution_time} segundos")