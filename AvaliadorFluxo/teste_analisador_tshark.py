import subprocess
import pyshark
URL_PCAP = "datasets/pcaps/trabalho1.pcapng"
TSHARK_PATH = "C:/Program Files/Wireshark/tshark.exe"


def main():
    arquivo = pyshark.FileCapture(URL_PCAP)
    print(arquivo._get_tshark_path())


if __name__ == "__main__":
    main()
