from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp1

MAC = '00:45:E2:CF:45:8F'
BROADCAST = 'ff:ff:ff:ff:ff:ff'

frame = Ether(
    src=MAC,
    dst=BROADCAST,
)

pacote = ARP(pdst='192.168.0.3')

pacote_final = frame / pacote
# pacote_final.show()

resposta = srp1(pacote_final, timeout=2, verbose=False)
resposta.show()
