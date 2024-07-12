from Models.Flow import Flow
from Models.Recurrence import Recurrence

class Evaluator:
    def __init__(self, weights: dict) -> None:
        '''
            This class is responsible for evaluating the recurrences
        '''
        self.weights = weights
        self.recurrences = {}
        self.destiny_simple_flows = {}
        self.origin_simple_flows = {}

    def remove_simples_flows(self, origin_key: str, destiny_key: str):
        if self.destiny_simple_flows.get(destiny_key):
            self.destiny_simple_flows.pop(destiny_key)
        if self.origin_simple_flows.get(origin_key):
            self.origin_simple_flows.pop(origin_key)

    def add_flow(self, flow: Flow):
        '''
            This method adds a flow to the recurrences or to the simple flows if it is not a recurrence yet
        '''
        list_name = [flow.src, flow.dst]
        list_name.sort()
        pre_name = list_name[0] + " <-> " + list_name[1] + " : "
        destiny_key = pre_name + flow.dport
        origin_key = pre_name + flow.sport

        # If the value of the dictionary is None, add it to the simple flows
        if self.recurrences.get(destiny_key):
            self.recurrences[destiny_key].add_flow(flow)
            return
        
        if self.recurrences.get(origin_key):
            self.recurrences[origin_key].add_flow(flow)
            return
        
        # If the value of the dictionary is in the destiny_simple_flows
        if self.destiny_simple_flows.get(destiny_key):
            recurrence = Recurrence(flow, destiny_key, self.weights)
            self.recurrences[destiny_key] = recurrence
            self.remove_simples_flows(origin_key, destiny_key)
            return
        
        # If the value of the dictionary is in the origin_simple_flows
        if self.origin_simple_flows.get(origin_key):
            recurrence = Recurrence(flow, origin_key, self.weights)
            self.recurrences[origin_key] = recurrence
            self.remove_simples_flows(origin_key, destiny_key)
            return

        self.destiny_simple_flows[destiny_key] = flow
        self.origin_simple_flows[origin_key] = flow