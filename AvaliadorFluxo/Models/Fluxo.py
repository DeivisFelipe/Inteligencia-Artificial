import IP
import scapy.all as scapy

class Fluxo:
    def __init__(self, packet: IP) -> None:
        self.src = packet.src
        self.sport = packet.get_TCP().sport
        self.dst = packet.dst
        self.dport = packet.get_TCP().dport
        self.start_time = None
        self.end_time = None
        self.data_bytes = 0
        self.transactions = []
        self.handshake_complete = False
        self.packet_count = 0

        # Inicializa o handshake
        # O SYN já aconteceu, agora esperamos o SYN, ACK em número
        self.handshake = {
            "SYN": {
                "seq": packet.get_TCP().seq,
                "ack": packet.get_TCP().ack,
                'end': True,
                'responsavel': packet.src
            },
            "SYN, ACK": {
                "seq": None,
                "ack": None,
                'end': False,
                'responsavel': packet.dst
            },
            "ACK": {
                "seq": None,
                "ack": None,
                'end': False,
                'responsavel': packet.src
            }
        }


    def add_transaction(self, packet: IP) -> None:
        self.end_time = packet.timestamp
        self.data_bytes += packet.total_length
        self.packet_count += 1
        self.transactions.append(packet)

    def add_packet(self, packet: IP) -> None:
        # Verifica se o handshake foi completado
        if self.handshake_complete:
            self.add_transaction(packet)
        else:


    def __str__(self) -> str:
        return f"Fluxo(src={self.src}, sport={self.sport}, dst={self.dst}, dport={self.dport}, start_time={self.start_time}, end_time={self.end_time}, data_bytes={self.data_bytes}, transactions={self.transactions}, handshake_complete={self.handshake_complete}, packet_count={self.packet_count})"
