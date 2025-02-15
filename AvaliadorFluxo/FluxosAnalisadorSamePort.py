# Autor: Deivis Felipe Guerreiro Fagundes
# Email: deivis.guerreiro@gmail.com
# Institute: UFSM - Federal University of Santa Maria
# Data: 2024-05-10
# Update: 2024-07-12

# Python imports

import matplotlib.pyplot as plt
from progress.bar import FillingCirclesBar
import subprocess
import time

# Models

from Models.Evaluator import Evaluator
from Models.Flow import Flow

# HIPERPARAMETERS

# Files
EVALUATION_JSON_FILE = "AvaliadorFluxo/Saida/Avaliacao.json"
EVALUATION_TXT_FILE = "AvaliadorFluxo/Saida/Avaliacao.txt"
FLOWS_FILE = "AvaliadorFluxo/Saida/saida.txt"
GRAPHS_DIR = "AvaliadorFluxo/Saida/Graficos"
PATH_TSHARK = "C:/Program Files/Wireshark/tshark.exe"
PATH_PCAP = 'Datasets/Pcaps/201904091200.pcap'
SORTED_FLOWS_FILE = "../large-pcap-analyzer/caidateste.txt"

# Plot
HIST_BIN_SIZE = 10

# percents maximum for the evaluation 0.2 = 20%, 0 - 1
PERCENT_NSPACKGES = 0.2
PERCENT_SBYTES = 0.2
PERCENT_NRPACKGES = 0.2
PERCENT_RBYTES = 0.2
PERCENT_NTPACKGES = 0.2
PERCENT_TBYTES = 0.2
PERCENT_DURATION = 0.2


# Quantity of flows to be considered possibly recurrent
MINIMUM_FLOWS = 10

# Minimum score to be considered recurrent
MINIMUM_SCORE = 7
# Maximum score
MAXIMUM_SCORE = 10

# Percent of flows that will be considered
PERCENT_FLOWS = 1 # min: 0.0, max: 1.0

# Minimums save file
MINIMUM_FLOWS_FILE = 10
MINIMUM_SCORE_FILE = 0
MINIMUM_HIT_FILE = 0
MINIMUM_MISS_FILE = 0
MINIMUM_PREDICTION_FILE = 5
MINIMUM_ACCURACY_FILE = 95

# Booleans
MAKE_EVALUATION_TXT = False
MAKE_EVALUATION_JSON = False
MAKE_FLOWS = False
MAKE_GRAPHS = True
MAKE_ORDERED_FLOWS = False

# Global variables
percents = {
    "nspackges": PERCENT_NSPACKGES,
    "sbytes": PERCENT_SBYTES,
    "nrpackges": PERCENT_NRPACKGES,
    "rbytes": PERCENT_RBYTES,
    "ntpackges": PERCENT_NTPACKGES,
    "tbytes": PERCENT_TBYTES,
    "duration": PERCENT_DURATION
}

# Evaluator
evaluator = Evaluator(percents, MINIMUM_FLOWS, MINIMUM_SCORE, MAXIMUM_SCORE)

def convert_bytes(value, unit):
    '''
        This function converts values to bytes
    '''

    if unit == "bytes":
        return value
    if unit == "kB":
        return value * 1024
    if unit == "MB":
        return value * 1024 * 1024
    if unit == "GB":
        return value * 1024 * 1024 * 1024
    if unit == "TB":
        return value * 1024 * 1024 * 1024 * 1024

    return value

def make_graphs():
    print("Making graphs...")
    # Total of hits and misses
    hits = 0
    misses = 0
    for recurrence in evaluator.recurrences.values():
        # Percore as recorrencias
        hits += recurrence.hits_count
        misses += recurrence.misses_count

    accuracy = (hits / (hits + misses)) * 100

    # Histograma de hits e misses
    plt.figure(figsize=(10, 5))
    plt.bar(["Hits", "Misses"], [hits, misses], color=["green", "red"])
    plt.title("Histogram of Hits and Misses")
    plt.xlabel("Hits and Misses")
    plt.ylabel("Quantity")
    plt.text(0, hits, f"Accuracy: {accuracy:.2f}% - {hits}", ha='center', va='bottom')
    plt.text(1, misses, f"Loss: {100 - accuracy:.2f}% - {misses}", ha='center', va='bottom')
    plt.savefig(f"{GRAPHS_DIR}/HistogramaHitAndMisses.png")

    print("Graphs made!")

def save_evaluation():
    if MAKE_EVALUATION_TXT:
        print("Saving output to txt file...")
        with open(EVALUATION_TXT_FILE, 'w') as f:
            for recurrence in evaluator.recurrences.values():
                # Se tiver mais de uma ocorrencia, printa
                if recurrence.total_flow >= MINIMUM_FLOWS_FILE and recurrence.score >= MINIMUM_SCORE_FILE and recurrence.hits_count >= MINIMUM_HIT_FILE and recurrence.misses_count >= MINIMUM_MISS_FILE and recurrence.predictions_count >= MINIMUM_PREDICTION_FILE and recurrence.accuracy >= MINIMUM_ACCURACY_FILE:
                    f.write("=" * 105 + "\n\n")
                    f.write(str(recurrence))
                    f.write("\n")
        print("Output saved successfully!")

    if MAKE_EVALUATION_JSON:
        print("Saving output to json file...")
        with open(EVALUATION_JSON_FILE, 'w') as f:
            f.write("{\n")
            f.write("\"recorrencias\": [\n")
            f.write(",\n".join([str(recurrence.getJson()) for recurrence in evaluator.recurrences.values() if recurrence.score >= MINIMUM_SCORE]))
            f.write("\n]\n")
            f.write("}\n")
        print("Output saved successfully!")

def start_evaluation():
    '''
        This function is responsible for starting the evaluation
    '''

    print("Initializing the evaluation")

    # Read the sorted flows file
    with open(SORTED_FLOWS_FILE, 'r') as f:
        lines = f.readlines()

        # Progress
        progress = 0
        # Total lines
        total_lines = len(lines)
        # Time the execution
        time_execution = time.time()
        # Quantity of flows to be considered
        number_flows = int(total_lines * PERCENT_FLOWS)
        percent = number_flows // 100

        bar = FillingCirclesBar('Evaluating', suffix='%(percent)d%% - %(eta)ds', max=100)

        for index, line in enumerate(lines[:number_flows]):

            # Update the progress
            if index != 0 and index % percent == 0 and progress < 100:
                progress += 1
                bar.next()

            slots = line.split()

            # src e a sport
            srcPort = slots[0].split(":")
            src = srcPort[0]
            sport = srcPort[1]

            # If it is ipv6, skip (srcPort has more than 3 elements)
            if len(srcPort) > 2:
                continue

            # dst e a dport
            dstPort = slots[2].split(":")
            dst = dstPort[0]
            dport = dstPort[1]

            # If it is ipv6, skip (dstPort has more than 3 elements)
            if len(dstPort) > 2:
                continue

            nspackges = int(slots[6])
            sbytes = convert_bytes(int(slots[7]), slots[8])

            nrpackges = int(slots[3])
            rbytes = convert_bytes(int(slots[4]), slots[5])

            ntpackges = int(slots[9])
            tbytes = convert_bytes(int(slots[10]), slots[11])

            rtime = float(slots[12].replace(",", "."))
            duration = float(slots[13].replace(",", "."))

            # Create a flow
            flow = Flow(src, sport, dst, dport, nspackges, sbytes, nrpackges, rbytes, ntpackges, tbytes, rtime, duration)
            evaluator.add_flow(flow)

        print("\nEvaluation finished!")
        print("Total flows: ", number_flows)
        print("Total recurrences: ", len(evaluator.recurrences))
        # Seconds in 2 decimal places
        print(f"Time execution: {time.time() - time_execution:.2f} seconds")

def make_ordered_flows():
    '''
        This function is responsible for ordering the flows file
    '''

    # Time the execution
    time_execution = time.time()

    # Do the reading of the flows file, eliminate the initial lines and sort by relative start
    with open(FLOWS_FILE, 'r') as f:
        lines = f.readlines()

        print("Ordering flows file...")

        # Ordena as lines pelo relative start
        lines = sorted(lines[5:-1], key=lambda x: float(x.split()[12].replace(",", ".")))

        print("Flows file ordered!")

        # Save the sorted flows file
        with open(SORTED_FLOWS_FILE, 'w') as f:
            print("Saving sorted flows file...")
            for line in lines:
                f.write(line)
            print("Sorted flows file saved!")

    print(f"Time execution to sort: {time.time() - time_execution:.2f} seconds")

def make_flows():
    """
        This function is responsible for generating the flow data using tshark
        It only takes the tcp flows from the PCAP file
    """

    # Time the execution
    time_execution = time.time()

    print("Generating flows...")

    subprocess.run([PATH_TSHARK, "-r", PATH_PCAP, "-Q", "-z", "conv,tcp", ">", FLOWS_FILE], shell=True)
    
    print("Flows generated!")

    print(f"Time execution to generate: {time.time() - time_execution:.2f} seconds")
    

if __name__ == '__main__':
    if MAKE_FLOWS:
        make_flows()
    if MAKE_ORDERED_FLOWS:
        make_ordered_flows()
    if MAKE_EVALUATION_TXT or MAKE_EVALUATION_JSON or MAKE_GRAPHS:
        start_evaluation()
        if MAKE_GRAPHS: 
            make_graphs()
        save_evaluation()