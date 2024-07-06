
import scapy.all as scapy
from Models.IP import IP
from Models.TCP import TCP
from Models.Fluxo import Fluxo

# Analisador
class Analisador():
    def __init__(self):
        self.fluxos_concluidos = []
        self.fluxos_fechados = []
        # Estatisticas
        self.quantidade_pacotes = {
            'total': 0,
            'tcp': 0,
            'udp': 0,
            'outros': 0
        }

    def add_TCP(self, pacote):
        self.quantidade_pacotes['tcp'] += 1
        self.quantidade_pacotes['total'] += 1
        pacote_ip = self.cria_IP(pacote)
        pacote_tcp = self.cria_TCP(pacote)
        pacote_ip /= pacote_tcp # Adiciona o pacote TCP ao IP

    def add_UDP(self, pacote):
        self.quantidade_pacotes['udp'] += 1
        self.quantidade_pacotes['total'] += 1

    def add_outros(self, pacote):
        self.quantidade_pacotes['outros'] += 1
        self.quantidade_pacotes['total'] += 1

    def cria_IP(self, pacote):
        pacote_ip_pcap = pacote[scapy.IP]
        src = pacote_ip_pcap.src # Origem
        dst = pacote_ip_pcap.dst # Destino
        total_length = pacote_ip_pcap.len # Tamanho total do pacote
        protocol = pacote_ip_pcap.proto # TCP ou UDP
        version = pacote_ip_pcap.version # IPv4 ou IPv6
        ihl = pacote_ip_pcap.ihl # Internet Header Length
        ttl = pacote_ip_pcap.ttl # Time to Live
        id = pacote_ip_pcap.id # Identificação
        flags = pacote_ip_pcap.flags # Flags
        offset = pacote_ip_pcap.frag # Offset
        checksum = pacote_ip_pcap.chksum # Checksum
        tos = pacote_ip_pcap.tos # Type of Service
        options = pacote_ip_pcap.options # Opções
        timestamp = pacote.time # Timestamp
        return IP(src, dst, total_length, protocol, version, ihl, ttl, id, flags, offset, checksum, tos, options, timestamp)
    
    def cria_TCP(self, pacote):
        pacote_tcp_pcap = pacote[scapy.TCP]
        sport = pacote_tcp_pcap.sport # Porta de origem
        dport = pacote_tcp_pcap.dport # Porta de destino
        seq = pacote_tcp_pcap.seq # Número de sequência
        ack = pacote_tcp_pcap.ack # Número de Acknowledgement
        data_offset = pacote_tcp_pcap.dataofs # Data Offset
        reserved = pacote_tcp_pcap.reserved # Reserved
        flags = pacote_tcp_pcap.flags # Flags
        window = pacote_tcp_pcap.window # Window
        checksum = pacote_tcp_pcap.chksum # Checksum
        urg_pointer = pacote_tcp_pcap.urgptr # Urgent Pointer
        options = pacote_tcp_pcap.options # Opções
        return TCP(sport, dport, seq, ack, data_offset, reserved, flags, window, checksum, urg_pointer, options)

# URL do PCAP
URL_PCAP = ".\datasets\pcaps\\trabalho1.pcapng"

def main():
    print("Começando a analisar os fluxos do PCAP")

    # Cria o analisador
    analisador = Analisador()
    
    # Abre o arquivo PCAP
    pacotes = scapy.rdpcap(URL_PCAP)

    # Printa o número de pacotes
    print("Número de pacotes no PCAP: ", len(pacotes))

    # Percorre os pacotes
    for pacote in pacotes:
        # verifica se é pacote TCP, UDP ou outros
        if pacote.haslayer(scapy.TCP):
            analisador.add_TCP(pacote)
        elif pacote.haslayer(scapy.UDP):
            analisador.add_UDP(pacote)
        else:
            analisador.add_outros(pacote)

        break

if __name__ == '__main__':
    main()