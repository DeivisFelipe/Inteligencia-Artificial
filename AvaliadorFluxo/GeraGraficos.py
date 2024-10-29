import matplotlib.pyplot as plt

ARQUIVO_FLUXOS_ORDENADOS = "AvaliadorFluxo/Saida/FluxosOrdenados-MAWI.txt"
PASTA_GRAFICOS = "AvaliadorFluxo/Saida/Graficos"
# PLOT
QUANTIDADE_FLUXOS_HISTOGRAMA = 10

def main():
    fluxos = []
    maior_duracao = 0
    menor_duracao = 9999999999999999
    maior_bytes = 0
    menor_bytes = 9999999999999999
    # Lê o arquivo de fluxos
    with open(ARQUIVO_FLUXOS_ORDENADOS, 'r') as f:
        linhas = f.readlines()
        # Pula as 5 primeiras linhas
        for index, linha in enumerate(linhas[0:]):
            # Separa a linha por espaços
            partes = linha.split()
            # Pega o src e a sport
            src_port = partes[0].split(":")
            if len(src_port) == 2:
                src = src_port[0]
                sport = src_port[1]
            else:
                # é ipv6
                sport = src_port[-1]
                # src é tudo menos a porta e os dois pontos
                src = partes[0][:-len(sport) - 1]

            # Pega o dst e a dport
            dst_port = partes[2].split(":")
            if len(dst_port) == 2:
                dst = dst_port[0]
                dport = dst_port[1]
            else:
                # é ipv6
                dport = dst_port[-1]
                # dst é tudo menos a porta e os dois pontos
                dst = partes[2][:-len(dport) - 1]
                
            # Pega a quantidade de bytes enviados e recebidos, verifica se é em bytes, kB, MB ou GB
            nspackges = int(partes[3])
            sbytes = int(partes[4])
            tsbytes = partes[5]
            if tsbytes == "kB":
                sbytes = sbytes * 1024
            elif tsbytes == "MB":
                sbytes = sbytes * 1024 * 1024
            elif tsbytes == "GB":
                sbytes = sbytes * 1024 * 1024 * 1024

            nrpackges = int(partes[6])
            rbytes = int(partes[7])
            trbytes = partes[8]
            if trbytes == "kB":
                rbytes = rbytes * 1024
            elif trbytes == "MB":
                rbytes = rbytes * 1024 * 1024
            elif trbytes == "GB":
                rbytes = rbytes * 1024 * 1024 * 1024

            ntpackges = int(partes[9])
            tbytes = int(partes[10])
            ttbytes = partes[11]
            if ttbytes == "kB":
                tbytes = tbytes * 1024

            rtime = float(partes[12].replace(",", "."))
            duration = float(partes[13].replace(",", "."))

            # Cria o fluxo
            fluxos.append((src, sport, dst, dport, nspackges, sbytes, nrpackges, rbytes, ntpackges, tbytes, rtime, duration))

            # Atualiza a maior e menor duração
            if duration > maior_duracao:
                maior_duracao = duration
            if duration < menor_duracao:
                menor_duracao = duration

            # Atualiza a maior e menor quantidade de bytes
            if tbytes > maior_bytes:
                maior_bytes = tbytes
            if tbytes < menor_bytes:
                menor_bytes = tbytes
    print("Total de fluxos: ", len(fluxos))
    print("Maior duração: ", maior_duracao)
    print("Menor duração: ", menor_duracao)
    print("Maior quantidade de bytes: ", maior_bytes)
    print("Menor quantidade de bytes: ", menor_bytes)

    NUMERO_INTERVALOS_DURACAO = 60
    intervalo_duracao = (maior_duracao - menor_duracao) / NUMERO_INTERVALOS_DURACAO
    intervalos_duracao = []
    for i in range(NUMERO_INTERVALOS_DURACAO):
        # duas casas decimais
        intervalos_duracao.append(round(menor_duracao + i * intervalo_duracao, 2))

    # print("Duracao intervalos: ", intervalosDuracao)

    NUMERO_INTERVALOS_BYTES = 60
    intervalo_bytes = (maior_bytes - menor_bytes) / NUMERO_INTERVALOS_BYTES
    intervalos_bytes = []
    for i in range(NUMERO_INTERVALOS_BYTES):
        # duas casas decimais
        intervalos_bytes.append(round(menor_bytes + i * intervalo_bytes, 2))

    # print("Bytes intervalos: ", intervalosBytes)

    # Contador
    contadorDuracao = [0 for i in range(NUMERO_INTERVALOS_DURACAO)]
    contadorBytes = [0 for i in range(NUMERO_INTERVALOS_BYTES)]
    contadorPacotes = [0 for i in range(NUMERO_INTERVALOS_DURACAO)]

    bytesSoma = [0 for i in range(NUMERO_INTERVALOS_DURACAO)]

    # Conta quantos fluxos estão em cada intervalo
    for fluxo in fluxos:
        index = 0
        duracao = fluxo[11]
        bytes = fluxo[9]
        pacotes = fluxo[8]
        for i in range(NUMERO_INTERVALOS_DURACAO):
            if duracao >= intervalos_duracao[i]:
                index = i
            else:
                break

        contadorDuracao[index] += 1
        contadorPacotes[index] += pacotes
        bytesSoma[index] += bytes

        index = 0
        
        # descobre em qual intervalo está
        for i in range(NUMERO_INTERVALOS_BYTES):
            if bytes >= intervalos_bytes[i]:
                index = i
            else:
                break

        contadorBytes[index] += 1
    
    # Cria o gráfico de linha com y em escala logarítmica
    plt.plot(intervalos_duracao, contadorDuracao)
    plt.yscale('log')
    plt.xlabel('Intervalos de duração')
    plt.ylabel('Quantidade de fluxos')
    plt.title('Histograma de duração dos fluxos')
    plt.savefig(PASTA_GRAFICOS + "/HistogramaDuracao.png")

    # Cria o gráfico de linha com y em escala logarítmica
    plt.clf()
    plt.plot(intervalos_bytes, contadorBytes)
    plt.yscale('log')
    plt.xlabel('Intervalos de bytes')
    plt.ylabel('Quantidade de fluxos')
    plt.title('Histograma de bytes dos fluxos')
    plt.savefig(PASTA_GRAFICOS + "/HistogramaBytes.png")

    # Tamanho médio dos pacotes
    # X igual a duracao 
    # Y igual a tamanho medio
    # Tamanho medio = bytes / pacotes
    tamanho_medio = []
    for i in range(NUMERO_INTERVALOS_DURACAO):
        if contadorPacotes[i] != 0:
            tamanho_medio.append(bytesSoma[i] / contadorPacotes[i])
    plt.clf()
    plt.plot(intervalos_duracao, tamanho_medio) 
    plt.xlabel('Intervalos de duração')
    plt.ylabel('Tamanho médio dos pacotes')
    plt.title('Tamanho médio dos pacotes em relação a duração')
    plt.savefig(PASTA_GRAFICOS + "/TamanhoMedioPacotes.png")

    # Número total de pacotes
    total_pacotes = sum(contadorPacotes)
    print("Total de pacotes: ", total_pacotes)
    # Número total de bytes
    total_bytes = sum(bytesSoma)
    print("Total de bytes: ", total_bytes)
    # Tamanho médio dos pacotes
    tamanho_medio = total_bytes / total_pacotes
    print("Tamanho médio dos pacotes: ", tamanho_medio)
    
    

if __name__ == '__main__':
    main()