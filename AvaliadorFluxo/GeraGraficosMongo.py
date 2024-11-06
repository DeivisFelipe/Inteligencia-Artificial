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

    # # Cria o gráfico de linha com y em escala logarítmica
    # plt.clf()
    # plt.plot(intervalos_bytes, contadorBytes)
    # plt.yscale('log')
    # plt.xlabel('Intervalos de bytes')
    # plt.ylabel('Quantidade de fluxos')
    # plt.title('Histograma de bytes dos fluxos - ' + NAME)
    # plt.savefig(PATH_GRAPHS + "/HistogramaBytes.png")

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
    for i in range(NUMBER_BINS_HISTOGRAMA):
        query = {"duration": {"$gte": duration_intervals[i], "$lt": duration_intervals[i + 1]}}
        duration_counters[i] = collection.count_documents(query)

    # Cria o gráfico de linha com y em escala logarítmica
    plt.plot(duration_intervals, duration_counters)
    plt.yscale('log')
    plt.xlabel('Intervalos de duração')
    plt.ylabel('Quantidade de fluxos')
    plt.title('Histograma de duração dos fluxos - ' + NAME)
    plt.savefig(PATH_GRAPHS + "/HistogramaDuracao.png")

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