from scapy.layers.inet import traceroute

caminho = traceroute('google.com', verbose=False)
print(caminho)
