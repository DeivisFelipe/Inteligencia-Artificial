# Autor: Deivis Felipe Guerreiro Fagundes
# Email: deivis.guerreiro@gmail.com
# Institute: UFSM - Federal University of Santa Maria
# Data: 2024-05-10
# Update: 2024-07-12

# Python imports

import matplotlib.pyplot as plt
import subprocess
import time

# Models

from AvaliadorFluxo.Models.Evaluator import Evaluator
from AvaliadorFluxo.Models.Flow import Flow

# HIPERPARAMETERS

# Files
EVALUATION_JSON_FILE = "AvaliadorFluxo/Saida/Avaliacao.json"
EVALUATION_TXT_FILE = "AvaliadorFluxo/Saida/Avaliacao.txt"
FLOWS_FILE = "AvaliadorFluxo/Saida/Fluxos.txt"
GRAPHS_DIR = "AvaliadorFluxo/Saida/Graficos"
PATH_TSHARK = "C:/Program Files/Wireshark/tshark.exe"
PATH_PCAP = 'Datasets/Pcaps/201904091200.pcap'
SORTED_FLOWS_FILE = "AvaliadorFluxo/Saida/FluxosOrdenados.txt"

# Plot
HIST_BIN_SIZE = 10

# Weights for the evaluation
WEIGHTS_NSPACKGES = 1
WEIGHTS_SBYTES = 1
WEIGHTS_NRPACKGES = 1
WEIGHTS_RBYTES = 1
WEIGHTS_NTPACKGES = 5
WEIGHTS_TBYTES = 5
WEIGHTS_DURATION = 3

# Quantity of flows to be considered possibly recurrent
MINIMUM_FLOWS = 5

# Minimum score to be considered recurrent
MINIMUM_SCORE = 7

# Percent of flows that will be considered
PERCENT_FLOWS = 0.3

# Booleans
MAKE_EVALUATION_TXT = True
MAKE_EVALUATION_JSON = False
MAKE_FLOWS = False
MAKE_GRAPHS = False
MAKE_ORDERED_FLOWS = False

# Global variables
weights = {
    "nspackges": WEIGHTS_NSPACKGES,
    "sbytes": WEIGHTS_SBYTES,
    "nrpackges": WEIGHTS_NRPACKGES,
    "rbytes": WEIGHTS_RBYTES,
    "ntpackges": WEIGHTS_NTPACKGES,
    "tbytes": WEIGHTS_TBYTES,
    "duration": WEIGHTS_DURATION
}

# Evaluator
evaluator = Evaluator(weights)

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
    x = []
    y = []
    for index, recurrence in evaluator.recurrences.items():
        x.append(recurrence.bytes)
        y.append(recurrence.ocorrencias)

    plt.scatter(x, y)
    plt.xlabel("Total bytes")
    plt.ylabel("Number of flows")
    plt.title("Number of flows x Total bytes")
    plt.savefig(f"{GRAPHS_DIR}/NumeroFluxosQuantidadeBytes.png")

    # Histogram of occurrences
    plt.clf()
    x = []
    for index, recurrence in evaluator.recurrences.items():
        if recurrence.total_flow >= HIST_BIN_SIZE:
            x.append(recurrence.total_flow)
    plt.hist(x, bins=100, edgecolor='black', histtype='bar')
    plt.xlabel("Total occurrences")
    plt.ylabel("Number of flows")
    plt.title("Total occurrences x Number of flows")
    plt.savefig(f"{GRAPHS_DIR}/HistogramaOcorrencias.png")

    print("Graphs made!")

def save_evaluation():
    if MAKE_EVALUATION_TXT:
        print("Saving output to txt file...")
        with open(EVALUATION_TXT_FILE, 'w') as f:
            for index, recurrence in evaluator.recurrences.items():
                # Se tiver mais de uma ocorrencia, printa
                if recurrence.score >= MINIMUM_SCORE:
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
        MINIMUM_FLOWS = int(total_lines * PERCENT_FLOWS)
        percent = MINIMUM_FLOWS // 100

        for index, line in enumerate(lines[:MINIMUM_FLOWS]):

            # Update the progress
            if index != 0 and index % percent == 0 and progress < 100:
                progress += 1
                print(f"Progress: {progress}%, index: {index}/{MINIMUM_FLOWS}, Number of recurrences: {len(evaluator.recurrences)}")

            slots = line.split()
            # src e a sport
            srcPort = slots[0].split(":")
            src = srcPort[0]
            sport = srcPort[1]

            # If it is ipv6, skip (srcPort has more than 3 elements)
            if len(srcPort) > 2:
                continue

            # dst e a dport
            dstPort = line[2].split(":")
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

        print("Evaluation finished!")
        print(f"Time execution: {time.time() - time_execution} seconds")

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

    print(f"Time execution to sort: {time.time() - time_execution} seconds")

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

    print(f"Time execution to generate: {time.time() - time_execution} seconds")
    

if __name__ == '__main__':
    if MAKE_FLOWS:
        make_flows()
    if MAKE_ORDERED_FLOWS:
        make_ordered_flows()
    start_evaluation()
    if MAKE_GRAPHS: 
        make_flows()