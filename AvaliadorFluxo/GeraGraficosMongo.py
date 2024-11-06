import matplotlib.pyplot as plt
import pymongo
import time

PATH_GRAPHS = "AvaliadorFluxo/Saida/Graficos/AnaliseCaida"
NAME = "Caida 01 MongoDB"
NUMBER_BINS_HISTOGRAMA = 60
DB_NAME = "fluxos_database"
COLLECTION_NAME = "caida_collection"

def main():
    # Conecta ao MongoDB
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Pega o maior e o menor tempo de duração e a maior e a menor quantidade de bytes usando queries
    bigger_duration = collection.find_one(sort=[("duration", pymongo.DESCENDING)])["duration"]
    smaller_duration = collection.find_one(sort=[("duration", pymongo.ASCENDING)])["duration"]
    bigger_bytes = collection.find_one(sort=[("nbytes_total", pymongo.DESCENDING)])["nbytes_total"]
    smaller_bytes = collection.find_one(sort=[("nbytes_total", pymongo.ASCENDING)])["nbytes_total"]

    print("Maior duração: ", bigger_duration)
    print("Menor duração: ", smaller_duration)
    print("Maior quantidade de bytes: ", bigger_bytes)
    print("Menor quantidade de bytes: ", smaller_bytes)

    # Gera os intervalos de duração e bytes
    duration_interval = (bigger_duration - smaller_duration) / NUMBER_BINS_HISTOGRAMA
    duration_intervals = []
    for i in range(NUMBER_BINS_HISTOGRAMA):
        duration_intervals.append(round(smaller_duration + i * duration_interval))

    bytes_interval = (bigger_bytes - smaller_bytes) / NUMBER_BINS_HISTOGRAMA
    bytes_intervals = []
    for i in range(NUMBER_BINS_HISTOGRAMA):
        bytes_intervals.append(round(smaller_bytes + i * bytes_interval))

    # Contadores
    duration_counters = [0 for i in range(NUMBER_BINS_HISTOGRAMA)]
    bytes_counters = [0 for i in range(NUMBER_BINS_HISTOGRAMA)]
    packets_counters = [0 for i in range(NUMBER_BINS_HISTOGRAMA)]
    total_bytes = [0 for i in range(NUMBER_BINS_HISTOGRAMA)]

    duration_histogram(collection, duration_intervals, duration_counters)
    bytes_histogram(collection, bytes_intervals, bytes_counters)

    # # Tamanho médio dos pacotes
    # # X igual a duracao 
    # # Y igual a tamanho medio
    # # Tamanho medio = bytes / pacotes
    # tamanho_medio = []
    # for i in range(NUMERO_INTERVALOS_DURACAO):
    #     if contadorPacotes[i] != 0:
    #         tamanho_medio.append(bytesSoma[i] / contadorPacotes[i])
    # plt.clf()
    # plt.plot(intervalos_duracao, tamanho_medio) 
    # plt.xlabel('Intervalos de duração')
    # plt.ylabel('Tamanho médio dos pacotes')
    # plt.title('Tamanho médio dos pacotes em relação a duração - ' + NAME)
    # plt.savefig(PATH_GRAPHS + "/TamanhoMedioPacotes.png")

    # # Número total de pacotes
    # total_pacotes = sum(contadorPacotes)
    # print("Total de pacotes: ", total_pacotes)
    # # Número total de bytes
    # total_bytes = sum(bytesSoma)
    # print("Total de bytes: ", total_bytes)
    # # Tamanho médio dos pacotes
    # tamanho_medio = total_bytes / total_pacotes
    # print("Tamanho médio dos pacotes: ", tamanho_medio)
    


# Greficos

# Histograma de duração dos fluxos
def duration_histogram(collection, duration_intervals, duration_counters):
    print("*" * 50)
    print("Gerando histograma de duração dos fluxos...")
    for i in range(NUMBER_BINS_HISTOGRAMA):
        if i == NUMBER_BINS_HISTOGRAMA - 1:
            query = {"duration": {"$gte": duration_intervals[i]}}
        else:
            query = {"duration": {"$gte": duration_intervals[i], "$lt": duration_intervals[i + 1]}}
        duration_counters[i] = collection.count_documents(query)

    # Cria o gráfico de histograma com y em escala logarítmica
    plt.figure(figsize=(10, 5))
    plt.bar(duration_intervals, duration_counters, color="blue", width=(duration_intervals[1] - duration_intervals[0]) * 0.8)
    plt.xlabel('Intervalos de duração')
    plt.ylabel('Quantidade de fluxos')
    plt.title('Histograma de duração dos fluxos - ' + NAME)
    plt.savefig(PATH_GRAPHS + "/HistogramaDuracao.png")
    print("Histograma de duração dos fluxos gerado com sucesso!")

def bytes_histogram(collection, bytes_intervals, bytes_counters):
    print("*" * 50)
    print("Gerando histograma de bytes dos fluxos...")
    for i in range(NUMBER_BINS_HISTOGRAMA):
        if i == NUMBER_BINS_HISTOGRAMA - 1:
            query = {"nbytes_total": {"$gte": bytes_intervals[i]}}
        else:
            query = {"nbytes_total": {"$gte": bytes_intervals[i], "$lt": bytes_intervals[i + 1]}}
        bytes_counters[i] = collection.count_documents(query)

    # Cria o gráfico de histograma com y em escala logarítmica
    plt.figure(figsize=(10, 5))
    plt.bar(bytes_intervals, bytes_counters, color="blue", width=(bytes_intervals[1] - bytes_intervals[0]) * 0.8)
    plt.yscale('log')
    plt.xlabel('Intervalos de bytes')
    plt.ylabel('Quantidade de fluxos')
    plt.title('Histograma de bytes dos fluxos - ' + NAME)
    plt.savefig(PATH_GRAPHS + "/HistogramaBytes.png")
    plt.show()  # Exibe o gráfico durante o desenvolvimento
    print("Histograma de bytes dos fluxos gerado com sucesso!")

if __name__ == '__main__':
    start_time = time.time()
    print("Iniciando a geração dos gráficos...")
    print("Horário:", time.strftime("%H:%M:%S", time.localtime(start_time)))
    print("=" * 50)
    main()
    print("=" * 50)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Tempo de execução: ", execution_time, " segundos")