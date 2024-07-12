import subprocess
import os
import time
import matplotlib.pyplot as plt

PATH_TSHARK = "C:/Program Files/Wireshark/tshark.exe"
PATH_PCAP = 'Datasets/Pcaps/201904091200.pcap'
ARQUIVO_FLUXOS = "AvaliadorFluxo/Saida/Fluxos.txt"
ARQUIVO_FLUXOS_ORDENADOS = "AvaliadorFluxo/Saida/FluxosOrdenados.txt"
ARQUIVO_SAIDA = "AvaliadorFluxo/Saida/Avaliacao.txt"
PASTA_GRAFICOS = "AvaliadorFluxo/Saida/Graficos"
# PLOT
QUANTIDADE_FLUXOS_HISTOGRAMA = 10

# Pesos de cada valor
PESO_NSPACKGES = 1
PESO_SBYTES = 1
PESO_NRPACKGES = 1
PESO_RBYTES = 1
PESO_NTPACKGES = 5
PESO_TBYTES = 5
PESO_DURATION = 3
# Pontuação minima
PONTUACAO_MINIMA = 7

# Quantidade de fluxos para ser considerado possivelmente recorrente
QUANTIDADE_FLUXOS = 5

# Pontuação mínima para ser considerado recorrente
PONTUACAO_MINIMA = 7

# Porcentagem de fluxos que serão considerados
PORCENTAGEM_FLUXOS = 0.3

# Boleanos
GERA_ARQUIVO_AVALIACAO_TXT = True
GERA_ARQUIVO_AVALIACAO_JSON = False
GERA_GRAFICOS = False


def gera_fluxos():
    """
        Essa função é responsável por gerar os dados dos fluxos utilizando o tshark
        Ele só pega os fluxos tcp do arquivo PCAP
    """

    # Tempo de execução
    tempo_inicial = time.time()
    print("Gerando arquivo de fluxos...")
    # Cria o subprocesso e salva no arquivo
    subprocess.run([PATH_TSHARK, "-r", PATH_PCAP, "-Q", "-z", "conv,tcp", ">", ARQUIVO_FLUXOS], shell=True)
    
    print("Arquivo de fluxos gerado com sucesso!")
    print(f"Tempo de execução: {time.time() - tempo_inicial} segundos")

    # Faz a leitura do arquivo de fluxos, elemina as linhas iniciais e faz a ordenação pelo relative start
    with open(ARQUIVO_FLUXOS, 'r') as f:
        linhas = f.readlines()
        print("Ordenando arquivo de fluxos...")
        # Ordena as linhas pelo relative start
        linhas = sorted(linhas[5:-1], key=lambda x: float(x.split()[12].replace(",", ".")))
        print("Arquivo de fluxos ordenado com sucesso!")

        # Salva as linhas ordenadas no arquivo
        with open(ARQUIVO_FLUXOS_ORDENADOS, 'w') as f:
            print("Salvando arquivo de fluxos ordenado...")
            for linha in linhas:
                f.write(linha)
            print("Arquivo de fluxos ordenado salvo com sucesso!")


class Fluxo:
    def __init__(self, src, sport, dst, dport, nspackges, sbytes, nrpackges, rbytes, ntpackges, tbytes, rtime, duration) -> None:
        """
            Essa classe representa um fluxo, com todas as suas informações
        """
        self.predicted = None
        self.src = src
        self.sport = sport
        self.dst = dst
        self.dport = dport
        self.nspackges = nspackges
        self.sbytes = sbytes
        self.nrpackges = nrpackges
        self.rbytes = rbytes
        self.ntpackges = ntpackges
        self.tbytes = tbytes
        self.rtime = rtime
        self.duration = duration

    def __str__(self) -> str:
        # predicted| src| sport| dst| dport| nspackges| sbytes| nrpackges| rbytes| ntpackges| tbytes| rtime| duration
        # cada campo com 10 caracteres
        return f"| {self.predicted:15} | {self.src:15} | {self.sport:10} | {self.dst:15} | {self.dport:10} | {self.nspackges:10} | {self.sbytes:10} | {self.nrpackges:10} | {self.rbytes:10} | {self.ntpackges:10} | {self.tbytes:10} | {self.rtime:10.2f} | {self.duration:10.2f} |"

    def getJson(self):
        return {
            "predicted": self.predicted,
            "src": self.src,
            "sport": self.sport,
            "dst": self.dst,
            "dport": self.dport,
            "nspackges": self.nspackges,
            "sbytes": self.sbytes,
            "nrpackges": self.nrpackges,
            "rbytes": self.rbytes,
            "ntpackges": self.ntpackges,
            "tbytes": self.tbytes,
            "rtime": self.rtime,
            "duration": self.duration
        }

class Recorrencia:
    def __init__(self, fluxo: Fluxo, chave: tuple) -> None:
        """
            Essa classe contêm os fluxos recorrentes, agrupando pela tupla
        """
        self.chave = chave
        self.src = fluxo.src
        self.dst = fluxo.dst
        self.sport = fluxo.sport
        self.dport = fluxo.dport
        self.rtime = fluxo.rtime

        # Médias dos valores
        self.npackges_media = fluxo.ntpackges
        self.bytes_media = fluxo.tbytes
        self.duration_media = fluxo.duration

        # Médias recorrencia
        self.nspackges_recorrencia_media = fluxo.nspackges
        self.sbytes_recorrencia_media = fluxo.sbytes
        self.nrpackges_recorrencia_media = fluxo.nrpackges
        self.rbytes_recorrencia_media = fluxo.rbytes
        self.npackges_recorrencia_media = fluxo.ntpackges
        self.bytes_recorrencia_media = fluxo.tbytes
        self.duration_recorrencia_media = fluxo.duration

        # Totais
        self.npackges = fluxo.ntpackges
        self.bytes = fluxo.tbytes
        self.duration = fluxo.duration

        self.ocorrencias = 1
        self.score = 0
        self.fluxos = [fluxo]

    def __str__(self) -> str:
        # Printa o cabeçalho da recorrencia
        recorrencia = "-" * 105 + "\n"
        recorrencia += f"| Chave:     | {self.chave:88} |\n"
        recorrencia += "-" * 105 + "\n"
        recorrencia += f"| Ocorrencias: {str(self.ocorrencias):88} |\n"
        # recorrencia += "-" * 105 + "\n"
        # recorrencia += f"| Pontuacao: {str(self.pontuacao):90} |\n"
        recorrencia += "-" * 105 + "\n"
        recorrencia += "|" + " " * 22 + " Medias" + " " * 22 + "|" + " " * 22 + " Totais" + " " * 22 + "|\n"
        recorrencia += "-" * 105 + "\n"
        recorrencia += "|        npackges |         bytes  |       duration |        npackges |         bytes  |       duration |\n"
        recorrencia += "-" * 105 + "\n"
        # Printa só no maximo 2 casas decimais
        recorrencia += f"| {self.npackges_media:15.2f} | {self.bytes_media:14.2f} | {self.duration_media:14.2f} | {self.npackges:15.2f} | {self.bytes:14.2f} | {self.duration:14.2f} |\n"
        recorrencia += "-" * 105 + "\n\n"
        
        # Divisa
        divisa = "*" * 105 + "\n"
        
        # Printa todos os fluxos
        # Faz o cabeçalho dos fluxos
        fluxos = "\n"
        fluxos += "-" * 167 + "\n"
        fluxos += "|" + " " * 79 + " Fluxos" + " " * 79 + "|\n" 
        fluxos += "-" * 167 + "\n"
        fluxos += "|             src |      sport |             dst |      dport |  nspackges |     sbytes |  nrpackges |     rbytes |  ntpackges |     tbytes |      rtime |   duration |\n"
        fluxos += "-" * 167 + "\n"
        fluxos += "\n".join([str(fluxo) for fluxo in self.fluxos])
        fluxos += "\n" + "-" * 167 + "\n"
        return recorrencia + divisa + fluxos
    
    def adiciona_fluxo(self, fluxo: Fluxo):
        #self.avalia(fluxo)
        self.recalcula_valores(fluxo)
        self.ocorrencias += 1
        self.rtime = fluxo.rtime
        self.fluxos.append(fluxo)

    def formula(self, fluxo: Fluxo) -> float:
        return 0

    def avalia(self, fluxo: Fluxo):
        pass

    def recalcula_valores(self, fluxo: Fluxo):
        # Faz a média dos valores, considerando a quantidade de ocorrencias
        # soma_nspackges = self.nspackges * (self.ocorrencias) + fluxo.nspackges
        # self.nspackges = soma_nspackges / (self.ocorrencias + 1)
        # soma_sbytes = self.sbytes * (self.ocorrencias) + fluxo.sbytes
        # self.sbytes = soma_sbytes / (self.ocorrencias + 1)
        # soma_nrpackges = self.nrpackges * (self.ocorrencias) + fluxo.nrpackges
        # self.nrpackges = soma_nrpackges / (self.ocorrencias + 1)
        # soma_rbytes = self.rbytes * (self.ocorrencias) + fluxo.rbytes
        # self.rbytes = soma_rbytes / (self.ocorrencias + 1)
        soma_npackges_media = self.npackges_media * (self.ocorrencias) + fluxo.ntpackges
        self.npackges_media = soma_npackges_media / (self.ocorrencias + 1)
        soma_bytes_media = self.bytes_media * (self.ocorrencias) + fluxo.tbytes
        self.bytes_media = soma_bytes_media / (self.ocorrencias + 1)
        soma_duration_media = self.duration_media * (self.ocorrencias) + fluxo.duration
        self.duration_media = soma_duration_media / (self.ocorrencias + 1)

        # Soma os valores aos totais
        self.npackges += fluxo.ntpackges
        self.bytes += fluxo.tbytes
        self.duration += fluxo.duration

    def getJson(self):
        return {
            "chave": self.chave,
            "ocorrencias": self.ocorrencias,
            "pontuacao": self.pontuacao,
            "fluxos": [fluxo.getJson() for fluxo in self.fluxos]
        }


class AvaliadorFluxo:
    def __init__(self) -> None:
        self.recorrencias = {}
        self.fluxos_simples_destino = {}
        self.fluxos_simples_origem = {}

    def remove_fluxos_simples(self, chave_origem, chave_destino):
        if self.fluxos_simples_destino.get(chave_destino):
            self.fluxos_simples_destino.pop(chave_destino)
        if self.fluxos_simples_origem.get(chave_origem):
            self.fluxos_simples_origem.pop(chave_origem)

    def adiciona_fluxo(self, fluxo: Fluxo):
        listaNome = [fluxo.src, fluxo.dst]
        listaNome.sort()
        prenome = listaNome[0] + " <-> " + listaNome[1] + " : "
        chave_destino = prenome + fluxo.dport
        chave_origem = prenome + fluxo.sport
        # Se o valor do dicionario for None, adiciona ele aos fluxos simples
        if not self.recorrencias.get(chave_destino):
            if not self.recorrencias.get(chave_origem):
                # Verifica se o fluxo destino está no fluxos_simples_destino
                if not self.fluxos_simples_destino.get(chave_destino):
                    # Verifica se o fluxo origem está no fluxos_simples_origem
                    if not self.fluxos_simples_origem.get(chave_origem):
                        self.fluxos_simples_destino[chave_destino] = fluxo
                        self.fluxos_simples_origem[chave_origem] = fluxo
                    else:
                        fluxo_encontrado = self.fluxos_simples_origem[chave_origem]
                        recorrencia = Recorrencia(fluxo_encontrado, chave_origem)
                        recorrencia.adiciona_fluxo(fluxo)
                        self.recorrencias[chave_origem] = recorrencia
                        self.remove_fluxos_simples(chave_origem, chave_destino)
                else:
                    fluxo_encontrado = self.fluxos_simples_destino[chave_destino]
                    recorrencia = Recorrencia(fluxo, chave_destino)
                    recorrencia.adiciona_fluxo(fluxo_encontrado)
                    self.recorrencias[chave_destino] = recorrencia
                    self.remove_fluxos_simples(chave_origem, chave_destino)

            else:
                recorrencia = self.recorrencias[chave_origem]
                recorrencia.adiciona_fluxo(fluxo)
        else:
            recorrencia = self.recorrencias[chave_destino]
            recorrencia.adiciona_fluxo(fluxo)

def main():
    # Cria o avaliador de fluxo
    avaliador = AvaliadorFluxo()
    # Lê o arquivo de fluxos
    with open(ARQUIVO_FLUXOS_ORDENADOS, 'r') as f:
        linhas = f.readlines()
        # Porcentagem de progresso
        progresso = 0
        # Quantidade de linhas
        quantidade_linhas = len(linhas)
        print("Analisando fluxos...")
        tempo_inicial = time.time()
        # Pega a quantidade de fluxos que serão considerados
        quantidade_fluxos = int(quantidade_linhas * PORCENTAGEM_FLUXOS)
        quantidade_porcentagem = quantidade_fluxos // 100
        # Pula as 5 primeiras linhas
        for index, linha in enumerate(linhas[0:quantidade_fluxos]):
            # Atualiza a porcentagem
            if index != 0 and index % quantidade_porcentagem == 0 and progresso < 100:
                progresso += 1
                print(f"Progresso: {progresso}%, index: {index}/{quantidade_fluxos}, numero de recorrencias: {len(avaliador.recorrencias)}")
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
            fluxo = Fluxo(src, sport, dst, dport, nspackges, sbytes, nrpackges, rbytes, ntpackges, tbytes, rtime, duration)
            
            # Adiciona o fluxo no avaliador
            avaliador.adiciona_fluxo(fluxo)

        print("Análise dos fluxos concluída!")
        print(f"Tempo de execução: {time.time() - tempo_inicial} segundos")

    if GERA_ARQUIVO_AVALIACAO_TXT:
        # Salva a saída em um arquivo
        print("Salvando saída em arquivo...")
        with open(ARQUIVO_SAIDA, 'w') as f:
            for index, recorrencia in avaliador.recorrencias.items():
                # Se tiver mais de uma ocorrencia, printa
                if recorrencia.score >= PONTUACAO_MINIMA:
                    f.write("=" * 105 + "\n\n")
                    f.write(str(recorrencia))
                    f.write("\n")

        print("Saída salva com sucesso!")

    if GERA_ARQUIVO_AVALIACAO_JSON:
        # Salva a saída em um arquivo json
        print("Salvando saída em arquivo json...")
        with open("AvaliadorFluxo/Saida/Avaliacao.json", 'w') as f:
            f.write("{\n")
            f.write("\"recorrencias\": [\n")
            f.write(",\n".join([str(recorrencia.getJson()) for recorrencia in avaliador.recorrencias.values() if recorrencia.score >= PONTUACAO_MINIMA]))
            f.write("\n]\n")
            f.write("}\n")

        print("Saída salva com sucesso!")

    if GERA_GRAFICOS:
        # Percorre todos os fluxos e faz um grafico de número de fluxos pela quantidade de bytes
        print("Gerando gráficos...")
        x = []
        y = []
        for index, recorrencia in avaliador.recorrencias.items():
            x.append(recorrencia.bytes)
            y.append(recorrencia.ocorrencias)

        # print(x, y)
        plt.scatter(x, y)
        plt.xlabel("Quantidade de bytes")
        plt.ylabel("Número de fluxos")
        plt.title("Número de bytes pela quantidade de fluxos")
        plt.savefig(f"{PASTA_GRAFICOS}/NumeroFluxosQuantidadeBytes.png")

        # Histograma de quantidade de ocorrencias
        # zera o plot
        plt.clf()
        x = []
        for index, recorrencia in avaliador.recorrencias.items():
            if recorrencia.ocorrencias >= QUANTIDADE_FLUXOS_HISTOGRAMA:
                x.append(recorrencia.ocorrencias)
        plt.hist(x, bins=100, edgecolor='black', histtype='bar')
        plt.xlabel("Quantidade de ocorrencias")
        plt.ylabel("Número de fluxos")
        plt.title("Histograma de quantidade de ocorrencias")
        plt.savefig(f"{PASTA_GRAFICOS}/HistogramaOcorrencias.png")

        print("Gráficos gerados com sucesso!")
    

if __name__ == '__main__':
    # se tiver o argumento --gera-fluxos, gera o arquivo de fluxos
    if '--gera-fluxos' in os.sys.argv:
        gera_fluxos()
    main()