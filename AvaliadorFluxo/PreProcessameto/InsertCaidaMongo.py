import pymongo
import time
from FluxoFile import FluxoFile

# Hiperparâmetros
PERMITIR_IPV6 = True
BATCH_SIZE = 1000000

file_name = "/home/deivis/Projetos/large-pcap-analyzer-2/caida01.txt"

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

db = mongo_client["fluxos_database"] # Cria a base de dados "fluxos_database" se ela não existir

collection = db["caida_collection"] # Cria a colecao "caida_collection" se ela não existir

# Pega o tempo inicial
start_time = time.time()

# Printa o início do processo
print("Inserindo os fluxos no banco de dados...")
print("Arquivo:", file_name)
print("Base de dados:", db.name)
print("Colecao:", collection.name)
print("Horario:", time.strftime("%H:%M:%S", time.localtime(start_time)))

batch = []

with open(file_name, "r") as file:
    for line in file:
        # 23.36.44.166:443 <-> 163.33.141.15:52079          0 0 bytes      36136 2385012 bytes      36136 2385012 bytes 0,000000  71,916941
        fluxo = FluxoFile(line, permitir_ipv6=PERMITIR_IPV6)

        if not PERMITIR_IPV6 and fluxo.ipv6:
            continue

        # Cria um dicionario com os dados do fluxo
        fluxo_dict = fluxo.to_dict()

        # Adiciona o dicionario ao lote
        batch.append(fluxo_dict)

        # Insere o dicionario na colecao
        if len(batch) == BATCH_SIZE:
            collection.insert_many(batch)
            batch = []
            print(f"Fluxos inseridos: {BATCH_SIZE}")

    # Insere o restante dos fluxos
    if batch:
        collection.insert_many(batch)

# Pega o tempo final
final_time = time.time()

# Calcula o tempo de execucao
execution_time = final_time - start_time

print(f"Tempo de execucao: {execution_time} segundos")