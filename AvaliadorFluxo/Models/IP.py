class IP:
    def __init__(self, src, dst, total_length, protocol, version, ihl, ttl, id, flags, offset, checksum, tos, options, timestamp=None):
        self.src = src
        self.dst = dst
        self.total_length = total_length
        self.protocol = protocol
        self.version = version
        self.ihl = ihl
        self.ttl = ttl
        self.id = id
        self.flags = flags
        self.offset = offset
        self.checksum = checksum
        self.tos = tos
        self.options = options
        self.timestamp = timestamp

    # adiciona o data com o operador / para que possamos concatenar os pacotes
    def __div__(self, other):
        self.data = other

    def get_TCP(self):
        return self.data


    def __str__(self):
        return f"IP(src={self.src}, dst={self.dst}, total_length={self.total_length}, protocol={self.protocol}, version={self.version}, ihl={self.ihl}, ttl={self.ttl}, id={self.id}, flags={self.flags}, offset={self.offset}, checksum={self.checksum}, tos={self.tos})"