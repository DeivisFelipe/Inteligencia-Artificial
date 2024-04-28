from scapy.layers.inet import IP, UDP
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp
from scapy.config import conf
from scapy.volatile import RandInt
# importa o get_if_raw_hwaddr
from scapy.arch import get_if_raw_hwaddr

meu_mac = get_if_raw_hwaddr(conf.iface)[1]

MAC = '00:45:E2:CF:45:8F'

pacote = Ether(src=conf.iface.mac, dst='ff:ff:ff:ff:ff:ff')
pacote /= IP(src='0.0.0.0', dst='255.255.255.255')
pacote /= UDP(sport=68, dport=67)
pacote /= BOOTP(chaddr=meu_mac, xid=RandInt())
pacote /= DHCP(
    options=[
        ('message-type', 'discover'),
        'end',
    ]
)

sendp(pacote, iface=conf.iface, verbose=False)
