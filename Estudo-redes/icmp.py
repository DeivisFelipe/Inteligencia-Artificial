from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import srp1

MAC = '00:45:E2:CF:45:8F'
MEU_IP = '192.168.0.231'

pacote = Ether()
pacote /= IP(dst='google.com')
pacote /= ICMP()

resposta = srp1(pacote, timeout=2, verbose=False)

resposta.show()
