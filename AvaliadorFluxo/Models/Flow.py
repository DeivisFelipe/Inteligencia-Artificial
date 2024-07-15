class Flow:
    def __init__(self, src: str, sport: str, dst: str, dport: str, nspackges: int, sbytes: int, nrpackges: int, rbytes: int, ntpackges: int, tbytes: int, rtime: float, duration: float) -> None:
        """
            This class represents a flow, with all its information
        """
        self.predicted = None
        self.similar = False
        self.id = 0
        self.error = ""
        self.score = 0
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
    
    def setError(self, field:str, value:float):
        self.error += f"{field} : {value:.0f}%"

    def similarity(self, flow, percents) -> bool:
        """ 
            This function calculates the similarity between two flows
        """
        
        # Calculate the percente of difference between the flows
        if self.nspackges == 0 and flow.nspackges != 0 or flow.nspackges == 0 and self.nspackges != 0:
            return False
        if self.nspackges != 0 and flow.nspackges != 0:
            diff_nspackges = abs(flow.nspackges - self.nspackges)
            # Verifica o quanto a diferença é em relação ao total em porcentagem
            percent_diff_nspackges = (diff_nspackges * 100) / flow.nspackges
            if percent_diff_nspackges > percents["nspackges"]:
                # Error with 2 decimal places
                self.setError("nspackges", percent_diff_nspackges)
                return False
        
        if self.sbytes == 0 and flow.sbytes != 0 or flow.sbytes == 0 and self.sbytes != 0:
            return False
        if self.sbytes != 0 and flow.sbytes != 0:
            diff_sbytes = abs(flow.sbytes - self.sbytes)
            percent_diff_sbytes = (diff_sbytes * 100) / flow.sbytes
            if percent_diff_sbytes > percents["sbytes"]:
                self.setError("sbytes", percent_diff_sbytes)
                return False
        
        if self.nrpackges == 0 and flow.nrpackges != 0 or flow.nrpackges == 0 and self.nrpackges != 0:
            return False
        if self.nrpackges != 0 and flow.nrpackges != 0:
            diff_nrpackges = abs(flow.nrpackges - self.nrpackges)
            percent_diff_nrpackges = (diff_nrpackges * 100) / flow.nrpackges
            if percent_diff_nrpackges > percents["nrpackges"]:
                self.setError("nrpackges", percent_diff_nrpackges)
                return False
        
        if self.rbytes == 0 and flow.rbytes != 0 or flow.rbytes == 0 and self.rbytes != 0:
            return False
        if self.rbytes != 0 and flow.rbytes != 0:
            diff_rbytes = abs(flow.rbytes - self.rbytes)
            percent_diff_rbytes = (diff_rbytes * 100) / flow.rbytes
            if percent_diff_rbytes > percents["rbytes"]:
                self.setError("rbytes", percent_diff_rbytes)
                return False
        
        if self.ntpackges == 0 and flow.ntpackges != 0 or flow.ntpackges == 0 and self.ntpackges != 0:
            return False
        if self.ntpackges != 0 and flow.ntpackges != 0:
            diff_ntpackges = abs(flow.ntpackges - self.ntpackges)
            percent_diff_ntpackges = (diff_ntpackges * 100) / flow.ntpackges
            if percent_diff_ntpackges > percents["ntpackges"]:
                self.setError("ntpackges", percent_diff_ntpackges)  
                return False
        
        if self.tbytes == 0 and flow.tbytes != 0 or flow.tbytes == 0 and self.tbytes != 0:
            return False
        if self.tbytes != 0 and flow.tbytes != 0:
            diff_tbytes = abs(flow.tbytes - self.tbytes)
            percent_diff_tbytes = (diff_tbytes * 100) / flow.tbytes
            if percent_diff_tbytes > percents["tbytes"]:
                self.setError("tbytes", percent_diff_tbytes)
                return False
        
        if self.duration == 0 and flow.duration != 0 or flow.duration == 0 and self.duration != 0:
            return False
        if self.duration != 0 and flow.duration != 0:
            diff_duration = abs(flow.duration - self.duration)
            percent_diff_duration = (diff_duration * 100) / flow.duration
            if percent_diff_duration > percents["duration"]:
                self.setError("duration", percent_diff_duration)
                return False
        
        self.similar = True
        return True


    def __str__(self) -> str:
        error = self.error if not self.predicted else ""
        if self.predicted is None:
            predicted = "          "
        else:
            predicted = "Yes       " if self.predicted else "No        "
        # predicted| error| src| sport| dst| dport| nspackges| sbytes| nrpackges| rbytes| ntpackges| tbytes| rtime| duration
        return f"| {self.id:7} | {predicted} | {self.error:20} | {self.score:6} | {self.src:15} | {self.sport:10} | {self.dst:15} | {self.dport:10} | {self.nspackges:10} | {self.sbytes:10} | {self.nrpackges:10} | {self.rbytes:10} | {self.ntpackges:10} | {self.tbytes:10} | {self.rtime:10.2f} | {self.duration:10.6f} |"

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