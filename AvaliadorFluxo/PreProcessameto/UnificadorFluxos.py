import pymongo
import time
from FluxoFile import FluxoFile

#  Hiperparâmetros
FILE_FLUXOS = "AvaliadorFluxo\caida2.txt"
DATA_BASE_NAME = "fluxos_database"
COLLECTION_NAME = "caida_collection"
TIMEOUT_LIMIT = 60 * 1000 * 1000 # 60 segundos
OFFSET = 60 * 1000 * 1000 # 60 segundos

# Conecta ao MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client[DATA_BASE_NAME]
collection = db[COLLECTION_NAME]

# Pega o tempo inicial
start_time = time.time()

# Printa o início do processo
print("Inserindo os fluxos no banco de dados...")
print("Arquivo:", FILE_FLUXOS)
print("Base de dados:", db.name)
print("Coleção:", collection.name)
print("Horário:", time.strftime("%H:%M:%S", time.localtime(start_time)))

# Abre o arquivo de fluxos
with open(FILE_FLUXOS, "r") as file:
    for line in file:

        flow = FluxoFile(line, True)

        # Faz uma query para ver se o fluxo já existe no banco de dados
        query = {
            "src": flow.src,
            "src_port": flow.src_port,
            "dst": flow.dst,
            "dst_port": flow.dst_port,
        }

        # Procura o fluxo no banco de dados ordenando pelo start
        result = collection.find_one(query, sort=[("start", pymongo.DESCENDING)])

        insert = False
        if result:
            final = result['start'] + result['duration']
            time_to_end = (OFFSET + flow.start) - final 
            if time_to_end < 0:
                insert = True
            else:
                if time_to_end > TIMEOUT_LIMIT:
                    print("Timeout")
                    insert = True
            
        if insert:
            collection.insert_one(flow.to_dict())
        else:
            # Atualiza o fluxo já existe para ter a duração correta
            # Calcula a nova duração
            new_duration = flow.start + flow.duration + OFFSET

            # Atualiza o fluxo
            collection.update_one(
                query,
                {
                    "$set": {
                        "duration": new_duration
                    }
                }
            )


# Pega o tempo final
final_time = time.time()

# Calcula o tempo de execução
execution_time = final_time - start_time

print(f"Tempo de execução: {execution_time} segundos")