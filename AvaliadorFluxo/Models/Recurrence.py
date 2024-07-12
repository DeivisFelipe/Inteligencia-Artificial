from Models.Flow import Flow

class Recurrence:
    def __init__(self, init_flow: Flow, key: tuple, weights: dict) -> None:
        """
            This class contains the recurrent flows grouped by the tuple
        """
        self.key = key
        self.weights = weights
        self.src = init_flow.src
        self.dst = init_flow.dst
        self.sport = init_flow.sport
        self.dport = init_flow.dport
        self.rtime = init_flow.rtime

        # Averages of the total flows
        self.average_npackges = 0
        self.average_bytes = 0
        self.average_duration = 0

        # Recurrence averages
        self.recurrence_average_nspackges = 0
        self.recurrence_average_sbytes = 0
        self.recurrence_average_nrpackges = 0
        self.recurrence_average_rbytes = 0
        self.recurrence_average_npackges = 0
        self.recurrence_average_bytes = 0
        self.recurrence_average_duration = 0

        # Totals
        self.npackges = 0
        self.bytes = 0
        self.duration = 0

        self.total_flow = 0
        self.score = 0
        self.flows = []
        
        self.add_flow(init_flow)

    def __str__(self) -> str:
        # Print the recurrence slot
        recurrence_slot = "-" * 105 + "\n"
        recurrence_slot += f"| Key:     | {self.key:88} |\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += f"| Total Flow: {str(self.total_flow):88} |\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += f"| Score: {str(self.score):90} |\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += "|" + " " * 22 + " Averages" + " " * 22 + "|" + " " * 22 + " Totals" + " " * 22 + "|\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += "|        npackges |         bytes  |       duration |        npackges |         bytes  |       duration |\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += f"| {self.average_npackges:15.2f} | {self.average_bytes:14.2f} | {self.average_duration:14.2f} | {self.npackges:15.2f} | {self.bytes:14.2f} | {self.duration:14.4f} |\n"
        recurrence_slot += "-" * 105 + "\n\n"

        horizontal_line = "*" * 105 + "\n"
        
        # Print the flows slot
        flows_slot = "\n"
        flows_slot += "-" * 167 + "\n"
        flows_slot += "|" + " " * 79 + " Flows" + " " * 79 + "|\n" 
        flows_slot += "-" * 167 + "\n"
        flows_slot += "|             src |      sport |             dst |      dport |  nspackges |     sbytes |  nrpackges |     rbytes |  ntpackges |     tbytes |      rtime |   duration |\n"
        flows_slot += "-" * 167 + "\n"
        flows_slot += "\n".join([str(flow) for flow in self.flows])
        flows_slot += "\n" + "-" * 167 + "\n"

        return recurrence_slot + horizontal_line + flows_slot
    
    def add_flow(self, flow: Flow) -> None:
        """
            Add a flow to the recurrence
        """
        self.evaluate_flow(flow)
        self.evaluate_stats(flow)
        self.total_flow += 1
        self.rtime = flow.rtime
        self.flows.append(flow)

    def formula(self, flow: Flow) -> float:
        return 0

    def evaluate_flow(self, flow: Flow):
        pass

    def evaluate_stats(self, flow: Flow):
        # Update the averages
        sum_average_npackges = self.average_npackges * (self.total_flow) + flow.ntpackges
        self.average_npackges = sum_average_npackges / (self.total_flow + 1)
        sum_average_bytes = self.average_bytes * (self.total_flow) + flow.tbytes
        self.average_bytes = sum_average_bytes / (self.total_flow + 1)
        sum_average_duration = self.average_duration * (self.total_flow) + flow.duration
        self.average_duration = sum_average_duration / (self.total_flow + 1)

        # Sum the total values
        self.npackges += flow.ntpackges
        self.bytes += flow.tbytes
        self.duration += flow.duration

    def getJson(self):
        return {
            "key": self.key,
            "total_flow": self.total_flow,
            "score": self.score,
            "flows": [flow.getJson() for flow in self.flows]
        }