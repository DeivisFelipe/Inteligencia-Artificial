import pymongo
import time
from FluxoFile import FluxoFile

# Hiperparâmetros
FILE_FLUXOS = "AvaliadorFluxo/Saida/FluxosOrdenados-Caida01.txt"
DATA_BASE_NAME = "fluxos_database"
COLLECTION_NAME = "caida_collection"
TIMEOUT_LIMIT = 10 * 1000  # 10 segundos em milissegundos
OFFSET = 60 * 1000         # 60 segundos em milissegundos

# Conecta ao MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client[DATA_BASE_NAME]
collection = db[COLLECTION_NAME]

# Cria índice para melhorar a busca
collection.create_index([("src", pymongo.ASCENDING),
                         ("src_port", pymongo.ASCENDING),
                         ("dst", pymongo.ASCENDING),
                         ("dst_port", pymongo.ASCENDING)])

# Carrega os fluxos em memória
with open(FILE_FLUXOS, "r") as file:
    lines = file.readlines()

# Tempo inicial
start_time = time.time()
print("Inserindo os fluxos no banco de dados...")
print("Arquivo:", FILE_FLUXOS)
print("Base de dados:", db.name)
print("Coleção:", collection.name)
print("Horário:", time.strftime("%H:%M:%S", time.localtime(start_time)))

# Prepara operações em lote
bulk_operations = []

# Estatisticas
total_inserted = 0
total_updated = 0
time_to_end_less_than_zero = 0

# Dados Exemplos
last_update_flow = None
last_new_flow_on_update = None
last_flow = None

for line in lines:
    flow = FluxoFile(line, True)
    last_flow = flow
    query = {
        "src": flow.src,
        "src_port": flow.src_port,
        "dst": flow.dst,
        "dst_port": flow.dst_port,
    }

    # Busca o fluxo mais recente com os mesmos parâmetros
    result = collection.find_one(query, sort=[("start", pymongo.DESCENDING)])

    insert = False  # Controle de inserção

    if result:
        final = result['start'] + result['duration']
        time_to_end = (OFFSET + flow.start) - final

        if time_to_end < 0:
            insert = True
            time_to_end_less_than_zero += 1
        elif time_to_end > TIMEOUT_LIMIT:
            insert = True
        else:
            total_updated += 1
            last_update_flow = result
            last_new_flow_on_update = flow
            # Se não deve inserir, atualiza a duração do fluxo existente
            new_duration = (OFFSET - result['start']) + (flow.start + flow.duration)
            bulk_operations.append(
                pymongo.UpdateOne(
                    query,
                    {"$set": {"duration": new_duration}}
                )
            )
    else:
        # Não encontrou fluxo correspondente, deve inserir o novo fluxo
        insert = True

    if insert:
        total_inserted += 1
        # Atualiza o tempo de início do fluxo
        flow.start += OFFSET
        bulk_operations.append(
            pymongo.InsertOne(flow.to_dict())
        )

# Executa operações em lote
if bulk_operations:
    collection.bulk_write(bulk_operations)

# Calcula o tempo de execução
execution_time = time.time() - start_time
print(f"Tempo de execução: {execution_time} segundos")

# Estatísticas
print("Total de fluxos:", len(lines))
print("Total de fluxos inseridos:", total_inserted)
print("Total de fluxos atualizados:", total_updated)
print("Total de fluxos com tempo negativo:", time_to_end_less_than_zero)

# Exibe os últimos fluxos inseridos e atualizados
print("========================================")
print("Último fluxo inserido:")
print(last_flow)
print("========================================")
print("Último fluxo atualizado:")
print(last_update_flow)
print("========================================")
print("Novo fluxo no último update:")
print(last_new_flow_on_update)
