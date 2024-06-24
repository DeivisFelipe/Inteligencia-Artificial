import subprocess
import os
import time

PATH_TSHARK = "C:/Program Files/Wireshark/tshark.exe"
PATH_PCAP = 'teste.pcap'
ARQUIVO_FLUXOS = "fluxos.txt"
ARQUIVO_FLUXOS_ORDENADOS = "fluxos_ordenados.txt"
ARQUIVO_SAIDA = "saida.txt"

# Pesos de cada valor
PESO_NSPACKGES = 1
PESO_SBYTES = 1
PESO_NRPACKGES = 1
PESO_RBYTES = 1
PESO_NTPACKGES = 1
PESO_TBYTES = 5
PESO_RTIME = 0
PESO_DURATION = 1

# Pontuação minima
PONTUACAO_MINIMA = 7
# Quantidade de fluxos que serão considerados
QUANTIDADE_FLUXOS = 2
# Tempo de vida de uma recorrencia
TEMPO_VIDA = 100

# Porcentagem de fluxos que serão considerados
PORCENTAGEM = 1

def gera_fluxos():
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
        # nspackges| sbytes| nrpackges| rbytes| ntpackges| tbytes| rtime| duration
        # cada campo com 10 caracteres
        return f"| {self.nspackges:10} | {self.sbytes:10} | {self.nrpackges:10} | {self.rbytes:10} | {self.ntpackges:10} | {self.tbytes:10} | {self.rtime:10.2f} | {self.duration:10.2f} |"

class Recorrencia:
    def __init__(self, fluxo: Fluxo) -> None:
        self.src = fluxo.src
        self.dst = fluxo.dst
        self.sport = fluxo.sport
        self.dport = fluxo.dport
        self.nspackges = fluxo.nspackges
        self.sbytes = fluxo.sbytes
        self.nrpackges = fluxo.nrpackges
        self.rbytes = fluxo.rbytes
        self.ntpackges = fluxo.ntpackges
        self.tbytes = fluxo.tbytes
        self.rtime = fluxo.rtime
        self.duration = fluxo.duration
        self.ocorrencias = 1
        self.pontuacao = 0
        self.fluxos = [fluxo]

    def __str__(self) -> str:
        # Printa o cabeçalho da recorrencia
        recorrencia = "-" * 105 + "\n"
        recorrencia += f"| Recorrencia: | {self.src}:{self.sport} -> {self.dst}:{self.dport:47} |\n"
        recorrencia += "-" * 105 + "\n"
        recorrencia += f"| Ocorrencias: {str(self.ocorrencias):88} |\n"
        recorrencia += "-" * 105 + "\n"
        recorrencia += f"| Pontuacao: {str(self.pontuacao):90} |\n"
        recorrencia += "-" * 105 + "\n"
        recorrencia += "|  nspackges |     sbytes |  nrpackges |     rbytes |  ntpackges |     tbytes |      rtime |   duration |\n"
        recorrencia += "-" * 105 + "\n"
        # Printa só no maximo 2 casas decimais
        recorrencia += f"| {self.nspackges:10.2f} | {self.sbytes:10.2f} | {self.nrpackges:10.2f} | {self.rbytes:10.2f} | {self.ntpackges:10.2f} | {self.tbytes:10.2f} | {self.rtime:10.2f} | {self.duration:10.2f} |\n"
        recorrencia += "-" * 105 + "\n\n"
        
        # Divisa
        divisa = "*" * 105 + "\n"
        
        # Printa todos os fluxos
        # Faz o cabeçalho dos fluxos
        fluxos = "\n"
        fluxos += "-" * 105 + "\n"
        fluxos += "|" + " " * 48 + " Fluxos" + " " * 48 + "|\n" 
        fluxos += "-" * 105 + "\n"
        fluxos += "|  nspackges |     sbytes |  nrpackges |     rbytes |  ntpackges |     tbytes |      rtime |   duration |\n"
        fluxos += "-" * 105 + "\n"
        fluxos += "\n".join([str(fluxo) for fluxo in self.fluxos])
        fluxos += "\n" + "-" * 105 + "\n"
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
        soma_nspackges = self.nspackges * (self.ocorrencias) + fluxo.nspackges
        self.nspackges = soma_nspackges / (self.ocorrencias + 1)
        soma_sbytes = self.sbytes * (self.ocorrencias) + fluxo.sbytes
        self.sbytes = soma_sbytes / (self.ocorrencias + 1)
        soma_nrpackges = self.nrpackges * (self.ocorrencias) + fluxo.nrpackges
        self.nrpackges = soma_nrpackges / (self.ocorrencias + 1)
        soma_rbytes = self.rbytes * (self.ocorrencias) + fluxo.rbytes
        self.rbytes = soma_rbytes / (self.ocorrencias + 1)
        soma_ntpackges = self.ntpackges * (self.ocorrencias) + fluxo.ntpackges
        self.ntpackges = soma_ntpackges / (self.ocorrencias + 1)
        soma_tbytes = self.tbytes * (self.ocorrencias) + fluxo.tbytes
        self.tbytes = soma_tbytes / (self.ocorrencias + 1)
        soma_duration = self.duration * (self.ocorrencias) + fluxo.duration
        self.duration = soma_duration / (self.ocorrencias + 1)


class AvaliadorFluxo:
    def __init__(self) -> None:
        self.recorrencias = {}

    def adiciona_fluxo(self, fluxo: Fluxo):
        tupla_recorrencia = (fluxo.src, fluxo.dst, fluxo.sport, fluxo.dport)
        # Se o valor do dicionario for None, cria uma nova recorrencia
        if not self.recorrencias.get(tupla_recorrencia):
            recorrencia = Recorrencia(fluxo)
            self.recorrencias[tupla_recorrencia] = recorrencia
        else:
            # Se a tupla já existe no conjunto, adicione ela ao conjunto existente
            recorrencia = self.recorrencias[tupla_recorrencia]
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
        quantidade_fluxos = int(quantidade_linhas * PORCENTAGEM)
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

    # Salva a saída em um arquivo
    print("Salvando saída em arquivo...")
    with open(ARQUIVO_SAIDA, 'w') as f:
        for index, recorrencia in avaliador.recorrencias.items():
            # Se tiver mais de uma ocorrencia, printa
            if recorrencia.ocorrencias >= QUANTIDADE_FLUXOS:
                f.write("=" * 105 + "\n\n")
                f.write(str(recorrencia))
                f.write("\n")
    print("Saída salva com sucesso!")

if __name__ == '__main__':
    # se tiver o argumento --gera-fluxos, gera o arquivo de fluxos
    if '--gera-fluxos' in os.sys.argv:
        gera_fluxos()
    main()