class TCP:
    def __init__(self, sport, dport, seq, ack, data_offset, reserved, flags, window, checksum, urg_pointer, options):
        self.sport = sport
        self.dport = dport
        self.seq = seq
        self.ack = ack
        self.data_offset = data_offset
        self.reserved = reserved
        self.flags = flags
        self.window = window
        self.checksum = checksum
        self.urg_pointer = urg_pointer
        self.options = options

    # adiciona o data com o operador / para que possamos concatenar os pacotes
    def __div__(self, other):
        self.data = other

    def __str__(self):
        return f"TCP(sport={self.sport}, dport={self.dport}, seq={self.seq}, ack={self.ack}, data_offset={self.data_offset}, reserved={self.reserved}, flags={self.flags}, window={self.window}, checksum={self.checksum}, urg_pointer={self.urg_pointer})"