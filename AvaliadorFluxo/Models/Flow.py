class Fluxo:
    def __init__(self, src: str, sport: str, dst: str, dport: str, nspackges: int, sbytes: int, nrpackges: int, rbytes: int, ntpackges: int, tbytes: int, rtime: float, duration: float) -> None:
        """
            This class represents a flow, with all its information
        """
        self.predicted = None
        self.src = src
        self.sport = sport
        self.dst = dst
        self.dport = dport
        self.nspackges = nspackges
        self.sbytes = sbytes
        self.nrpackges = nrpackges
        self.rbytes = rbytes
        self.ntpackges = ntpackges
        self.tbytes = tbytes
        self.rtime = rtime
        self.duration = duration

    def __str__(self) -> str:
        # predicted| src| sport| dst| dport| nspackges| sbytes| nrpackges| rbytes| ntpackges| tbytes| rtime| duration
        return f"| {self.predicted:15} | {self.src:15} | {self.sport:10} | {self.dst:15} | {self.dport:10} | {self.nspackges:10} | {self.sbytes:10} | {self.nrpackges:10} | {self.rbytes:10} | {self.ntpackges:10} | {self.tbytes:10} | {self.rtime:10.2f} | {self.duration:10.4f} |"

    def getJson(self):
        return {
            "predicted": self.predicted,
            "src": self.src,
            "sport": self.sport,
            "dst": self.dst,
            "dport": self.dport,
            "nspackges": self.nspackges,
            "sbytes": self.sbytes,
            "nrpackges": self.nrpackges,
            "rbytes": self.rbytes,
            "ntpackges": self.ntpackges,
            "tbytes": self.tbytes,
            "rtime": self.rtime,
            "duration": self.duration
        }