from threading import Timer
import ConfigParser
from ControlFileScanner import ControlFileScanner
from AstmThreadedClient import AstmThreadedClient


PARAMETER_INI_FILE = "Parameters.CFG"
COMMUNICATION_SECTION_NAME = "Communication"
HOST_ADDRESS = "Host Address"
CONNECT_PORT = "Connect Port"
FLEXLAB36_CONFIG_FOLDER_PATH = "Flexlab36 Config Folder Path"

FILE_SCAN_INTERVAL = 5 # scan control log file time interval in seconds


class TimingScanner(ControlFileScanner):
    def __init__(self):
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        self.host_address = ''
        self.connect_port  = 8888
        self.control_folder = ""
        self.load_communication_parameters_from_config_file()
        ControlFileScanner.__init__(self, self.control_folder)
        self.astm_client = AstmThreadedClient(host_address=self.host_address, port=self.connect_port)

    def timing_exec_func(self):
        self.read_control_file_contents()
        self.scan_control_file_for_position_info()
        self.construct_sample_flag_from_position()
        self.send_flag_info()
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        self.timer.start()

    def send_flag_info(self):
        for sample_flag_info in self.sample_flag_info_list:
            self.astm_client.send_sample_las_flag(sample_flag_info)
            print sample_flag_info
        self.astm_client.trigger_a_sending()

    def start_timing_scanner(self):
        self.timer.start()

    def load_communication_parameters_from_config_file(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(PARAMETER_INI_FILE)
        if config_parser.has_section(COMMUNICATION_SECTION_NAME):
            self.host_address = config_parser.get(COMMUNICATION_SECTION_NAME,HOST_ADDRESS)
            self.connect_port = config_parser.getint(COMMUNICATION_SECTION_NAME,CONNECT_PORT)
            self.control_folder = config_parser.get(COMMUNICATION_SECTION_NAME,FLEXLAB36_CONFIG_FOLDER_PATH)

if __name__ == "__main__":
    scanner = TimingScanner()
    scanner.start_timing_scanner()
