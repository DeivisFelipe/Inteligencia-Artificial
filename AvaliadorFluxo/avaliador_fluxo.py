
import sys
import os
import scapy.all as scapy

# URL do PCAP
URL_PCAP = ".\datasets\pcaps\\trabalho1.pcapng"

def main():
    print("Começando a analisar os fluxos do PCAP")
    
    # Abre o arquivo PCAP
    pacotes = scapy.rdpcap(URL_PCAP)

    # Printa o número de pacotes
    print("Número de pacotes: ", len(pacotes))

    # Percorre os pacotes
    for pacote in pacotes:
        # verifica se é pacote TCP ou UDP
        if pacote.haslayer(scapy.TCP):
            # Passa o pacote para a classe de pacote TCP
            if isinstance(pacote, scapy.packet.Packet):
                    print(pacote.sprintf)
            pacote_tcp = pacote[scapy.TCP]

            # Se a flag SYN estiver setada printa uma mensagem
            if pacote_tcp.flags == 2:
                print("Pacote TCP com flag SYN setada")
                # print(pacote_tcp.show())
                # verifica se é uuma instancia de scapy.packet.Packet
            elif pacote_tcp.flags == 16:
                print("Pacote TCP com flag ACK setada")
                # print(pacote_tcp.show())
                
        elif pacote.haslayer(scapy.UDP):
            # Passa o pacote para a classe de pacote UDP
            pacote_udp = pacote[scapy.UDP]



if __name__ == '__main__':
    main()