from Models.Flow import Flow

class Recurrence:
    def __init__(self, init_flow: Flow, key: tuple, percents: dict, MINIMUM_FLOWS: int, MINIMUM_SCORE: int, MAXIMUM_SCORE: int) -> None:
        """
            This class contains the recurrent flows grouped by the tuple
        """
        self.key = key
        self.percents = percents
        self.MINIMUM_FLOWS = MINIMUM_FLOWS
        self.MINIMUM_SCORE = MINIMUM_SCORE
        self.MAXIMUM_SCORE = MAXIMUM_SCORE
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

        self.predictions_count = 0
        self.hits_count = 0
        self.misses_count = 0
        self.accuracy = 0
        self.total_flow = 0
        self.score = 0
        self.flows = []
        
        self.add_flow(init_flow)

    def __str__(self) -> str:
        # Print the recurrence slot
        recurrence_slot = "-" * 105 + "\n"
        recurrence_slot += f"| Key:     | {self.key:90} |\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += f"| Total Flow: {str(self.total_flow):89} |\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += f"| Score: {str(self.score):94} |\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += "|" + " " * 8 + " Predictions" + " " * 9 + "|" + " " * 8 + " Hits" + " " * 9 + "|" + " " * 8 + " Misses" + " " * 9  + "|" + " " * 8 + " Accuracy" + " " * 8 + "|\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += "|" + f"{self.predictions_count:29}" + "|" + f"{self.hits_count:22}" + "|" + f"{self.misses_count:24}" + "|" + f"{self.accuracy:25.2f}" + "|\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += "|" + " " * 22 + " Averages" + " " * 21 + "|" + " " * 22 + " Totals" + " " * 21 + "|\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += "|        npackges |         bytes  |       duration |        npackges |         bytes  |       duration |\n"
        recurrence_slot += "-" * 105 + "\n"
        recurrence_slot += f"| {self.average_npackges:15.2f} | {self.average_bytes:14.2f} | {self.average_duration:14.2f} | {self.npackges:15.2f} | {self.bytes:14.2f} | {self.duration:14.4f} |\n"
        recurrence_slot += "-" * 105 + "\n\n"

        horizontal_line = "*" * 105 + "\n"
        
        # Print the flows slot
        flows_slot = "\n"
        flows_slot += "-" * 222 + "\n"
        flows_slot += "|" + " " * 107 + " Flows" + " " * 107 + "|\n" 
        flows_slot += "-" * 222 + "\n"
        flows_slot += "|      id |  predicted |                error |  score |             src |      sport |             dst |      dport |  nspackges |     sbytes |  nrpackges |     rbytes |  ntpackges |     tbytes |      rtime |   duration |\n"
        flows_slot += "-" * 222 + "\n"
        flows_slot += "\n".join([str(flow) for flow in self.flows])
        flows_slot += "\n" + "-" * 222 + "\n"

        return recurrence_slot + horizontal_line + flows_slot
    
    def update_accuracy(self):
        if self.predictions_count > 0:
            self.accuracy = (self.hits_count * 100) / self.predictions_count
    
    def add_flow(self, flow: Flow) -> None:
        """
            Add a flow to the recurrence
        """
        self.evaluate_flow(flow)
        self.evaluate_stats(flow)
        self.total_flow += 1
        flow.id = self.total_flow
        self.flows.append(flow)
        self.update_accuracy()

    def evaluate_flow(self, flow: Flow):
        """
            Evaluate the flow and set the predicted value
        """
        # If the number of flows is iguals or greater than the minimum flows, evaluate de means of the self.MINIMUM_FLOWS last flows
        if self.total_flow >= self.MINIMUM_FLOWS:

            
            nspackges = 0
            sbytes = 0
            nrpackges = 0
            rbytes = 0
            ntpackges = 0
            tbytes = 0
            duration = 0
            
            # Get the last MINIMUM_FLOWS flows
            last_flows = self.flows[-self.MINIMUM_FLOWS:]

            # Sum the values
            for flow_last in last_flows:
                nspackges += flow_last.nspackges
                sbytes += flow_last.sbytes
                nrpackges += flow_last.nrpackges
                rbytes += flow_last.rbytes
                ntpackges += flow_last.ntpackges
                tbytes += flow_last.tbytes
                duration += flow_last.duration

            # Calculate the averages
            nspackges /= self.MINIMUM_FLOWS
            sbytes /= self.MINIMUM_FLOWS
            nrpackges /= self.MINIMUM_FLOWS
            rbytes /= self.MINIMUM_FLOWS
            ntpackges /= self.MINIMUM_FLOWS
            tbytes /= self.MINIMUM_FLOWS
            duration /= self.MINIMUM_FLOWS

            # Create a flow with the averages
            avarege_flow = Flow(self.src, self.sport, self.dst, self.dport, nspackges, sbytes, nrpackges, rbytes, ntpackges, tbytes, self.rtime, duration)

            # Get if is similar or not
            similar = flow.similarity(avarege_flow, self.percents)

            if similar:
                if self.score >= self.MINIMUM_SCORE:
                    flow.predicted = True
                    self.predictions_count += 1
                    self.hits_count += 1
                self.score += 1
                if self.score > self.MAXIMUM_SCORE:
                    self.score = self.MAXIMUM_SCORE
            else:
                if self.score >= self.MINIMUM_SCORE:
                    flow.predicted = False
                    self.predictions_count += 1
                    self.misses_count += 1
                self.score -= 1
                if self.score < 0:
                    self.score = 0
            
        flow.score = self.score
                


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