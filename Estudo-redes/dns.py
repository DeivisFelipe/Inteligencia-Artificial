from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1

pacote = IP(dst='181.213.132.2')
pacote /= UDP(dport=53)
pacote /= DNS(
    qd=DNSQR(qname='google.com')
)

resposta = sr1(pacote)
resposta.show()
