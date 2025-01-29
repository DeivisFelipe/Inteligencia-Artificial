import pymongo
import time
from FluxoFile import FluxoFile

# Hiperparametros
FILES_FLUXOS = [
    './Datasets/Fluxos/CAIDA/caida02.txt',
    './Datasets/Fluxos/CAIDA/caida03.txt',
    './Datasets/Fluxos/CAIDA/caida04.txt',
]

DATA_BASE_NAME = "fluxos_database"
COLLECTION_NAME = "caida_collection"
TIMEOUT_LIMIT = 20 * 1000  # 20 segundos em milissegundos
OFFSET = 60 * 1000         # 60 segundos em milissegundos
BATCH_SIZE = 1000000

# Conecta ao MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client[DATA_BASE_NAME]
collection = db[COLLECTION_NAME]

# Cria indices
collection.create_index([
    ("src", pymongo.ASCENDING),
    ("src_port", pymongo.ASCENDING),
    ("dst", pymongo.ASCENDING),
    ("dst_port", pymongo.ASCENDING),
    ("start", pymongo.DESCENDING),
])

actual_offset = OFFSET

print("Base de dados:", db.name)
print("Colecao:", collection.name)

# Percorre os arquivos de fluxos
for file_name in FILES_FLUXOS:
    # Tempo inicial
    start_time = time.time()
    print("Inserindo os fluxos no banco de dados...")
    print("Arquivo:", file_name)
    print("Horario:", time.strftime("%H:%M:%S", time.localtime(start_time)))

    # Prepara operacoes em lote
    bulk_operations = []

    # Estatisticas
    total_inserted = 0
    total_updated = 0
    time_to_end_less_than_zero = 0

    # Carrega os fluxos em memoria
    with open(file_name, "r") as file:
        for line in file:
            flow = FluxoFile(line, True)
            query = {
                "src": flow.src,
                "src_port": flow.src_port,
                "dst": flow.dst,
                "dst_port": flow.dst_port,
            }

            # Busca o fluxo mais recente com os mesmos parametros
            result = collection.find_one(query, sort=[("start", pymongo.DESCENDING)])

            insert = False  # Controle de insercoes

            if result:
                final = result['start'] + result['duration']
                time_to_end = (actual_offset + flow.start) - final

                if time_to_end < 0:
                    insert = True
                    time_to_end_less_than_zero += 1
                elif time_to_end > TIMEOUT_LIMIT:
                    insert = True
                else:
                    total_updated += 1
                    # Se nao deve inserir, atualiza a duracao do fluxo existente
                    new_duration = (actual_offset - result['start']) + (flow.start + flow.duration)
                    bulk_operations.append(
                        pymongo.UpdateOne(
                            {"_id": result["_id"]},  # Atualiza diretamente pelo ID
                            {"$set": {"duration": new_duration}}
                        )
                    )
            else:
                # Nao encontrou fluxo correspondente, deve inserir o novo fluxo
                insert = True

            if insert:
                total_inserted += 1
                # Atualiza o tempo de inicio do fluxo
                flow.start += actual_offset
                bulk_operations.append(
                    pymongo.InsertOne(flow.to_dict())
                )

            if len(bulk_operations) == BATCH_SIZE:
                collection.bulk_write(bulk_operations)
                bulk_operations = []
                # Tempo em segundos para inserir BATCH_SIZE fluxos
                time_to_insert = time.time() - start_time
                print(f"Fluxos inseridos: {BATCH_SIZE} - Tempo: {time_to_insert} segundos")

        # Executa operacoes em lote
        if bulk_operations:
            collection.bulk_write(bulk_operations)

        # Calcula o tempo de execucoes
        execution_time = time.time() - start_time
        print(f"Tempo de execucoes: {execution_time} segundos")

        # Exibe estatisticas
        print("Total de fluxos:", total_inserted + total_updated)
        print("Total de fluxos inseridos:", total_inserted)
        print("Total de fluxos atualizados:", total_updated)
        print("Total de fluxos com tempo negativo:", time_to_end_less_than_zero)

        actual_offset += OFFSET
