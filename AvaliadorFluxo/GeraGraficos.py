import subprocess
import os
import time
import matplotlib.pyplot as plt

ARQUIVO_FLUXOS_ORDENADOS = "AvaliadorFluxo/Saida/FluxosOrdenados-MAWI.txt"
PASTA_GRAFICOS = "AvaliadorFluxo/Saida/Graficos"
# PLOT
QUANTIDADE_FLUXOS_HISTOGRAMA = 10

def main():
    fluxos = []
    maiorDuracao = 0
    menorDuracao = 9999999999999999
    maiorBytes = 0
    menorBytes = 9999999999999999
    # Lê o arquivo de fluxos
    with open(ARQUIVO_FLUXOS_ORDENADOS, 'r') as f:
        linhas = f.readlines()
        # Pula as 5 primeiras linhas
        for index, linha in enumerate(linhas[0:]):
            # Separa a linha por espaços
            partes = linha.split()
            # Pega o src e a sport
            srcPort = partes[0].split(":")
            src = srcPort[0]
            sport = srcPort[1]

            # Se for ipv6, pula (srcPort tem mais de 3 elementos)
            if len(srcPort) > 2:
                continue
            # Pega o dst e a dport
            dstPort = partes[2].split(":")
            dst = dstPort[0]
            dport = dstPort[1]
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
            if duration > maiorDuracao:
                maiorDuracao = duration
            if duration < menorDuracao:
                menorDuracao = duration

            # Atualiza a maior e menor quantidade de bytes
            if tbytes > maiorBytes:
                maiorBytes = tbytes
            if tbytes < menorBytes:
                menorBytes = tbytes
    print("Total de fluxos: ", len(fluxos))
    print("Maior duração: ", maiorDuracao)
    print("Menor duração: ", menorDuracao)
    print("Maior quantidade de bytes: ", maiorBytes)
    print("Menor quantidade de bytes: ", menorBytes)

    NUMERO_INTERVALOS_DURACAO = 60
    intervaloDuracao = (maiorDuracao - menorDuracao) / NUMERO_INTERVALOS_DURACAO
    intervalosDuracao = []
    for i in range(NUMERO_INTERVALOS_DURACAO):
        # duas casas decimais
        intervalosDuracao.append(round(menorDuracao + i * intervaloDuracao, 2))

    # print("Duracao intervalos: ", intervalosDuracao)

    NUMERO_INTERVALOS_BYTES = 60
    intervaloBytes = (maiorBytes - menorBytes) / NUMERO_INTERVALOS_BYTES
    intervalosBytes = []
    for i in range(NUMERO_INTERVALOS_BYTES):
        # duas casas decimais
        intervalosBytes.append(round(menorBytes + i * intervaloBytes, 2))

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
            if duracao >= intervalosDuracao[i]:
                index = i
            else:
                break

        contadorDuracao[index] += 1
        contadorPacotes[index] += pacotes
        bytesSoma[index] += bytes

        index = 0
        
        # descobre em qual intervalo está
        for i in range(NUMERO_INTERVALOS_BYTES):
            if bytes >= intervalosBytes[i]:
                index = i
            else:
                break

        contadorBytes[index] += 1

    # print("Contador Duracao: ", contadorDuracao)
    # print("Contador Bytes: ", contadorBytes)
    # print("Contador Tamanho Médio: ", contadorTamanhoMedio)
    # print("Duracoes: ", bytesSoma)
    

    # Cria o gráfico de linha com y em escala logarítmica
    plt.plot(intervalosDuracao, contadorDuracao)
    plt.yscale('log')
    plt.xlabel('Intervalos de duração')
    plt.ylabel('Quantidade de fluxos')
    plt.title('Histograma de duração dos fluxos')
    plt.savefig(PASTA_GRAFICOS + "/HistogramaDuracao.png")

    # Cria o gráfico de linha com y em escala logarítmica
    plt.clf()
    plt.plot(intervalosBytes, contadorBytes)
    plt.yscale('log')
    plt.xlabel('Intervalos de bytes')
    plt.ylabel('Quantidade de fluxos')
    plt.title('Histograma de bytes dos fluxos')
    plt.savefig(PASTA_GRAFICOS + "/HistogramaBytes.png")

    # Tamanho médio dos pacotes
    # X igual a duracao 
    # Y igual a tamanho medio
    # Tamanho medio = bytes / pacotes
    for i in range(NUMERO_INTERVALOS_DURACAO):
        if contadorPacotes[i] != 0:
            contadorPacotes[i] = bytesSoma[i] / contadorPacotes[i]
    print("Contador médio de pacotes", contadorPacotes)
    plt.clf()
    plt.plot(intervalosDuracao, contadorPacotes) 
    plt.xlabel('Intervalos de duração')
    plt.ylabel('Tamanho médio dos pacotes')
    plt.title('Tamanho médio dos pacotes em relação a duração')
    plt.savefig(PASTA_GRAFICOS + "/TamanhoMedioPacotes.png")
    
    

if __name__ == '__main__':
    main()