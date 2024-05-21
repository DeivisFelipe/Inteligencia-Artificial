from sys import exit
from scapy.sendrecv import sniff


def resumo(x):
    return x.show()


try:
    sniff(prn=resumo, filter="dchp")
except KeyboardInterrupt:
    print('Fim do sniffing')
    exit(0)
