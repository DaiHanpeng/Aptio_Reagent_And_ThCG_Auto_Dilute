import os

from  SampleInlabbingPosition import SampleInlabbingPosition
from SamplePosition2FlagStratege import SamplePosition2FlagStratege
from ReagentStatusUpdateStrategy import ReagentStatusUpdateStrategy
from LoggingConfig import project_logger
from GetLatestPackedControlFile import GetLatestPackedControlFile
from Aptio_Reagent_Info import *


CONTROL_FILE = 'control.txt'
ASCII_SPACE = b'\x20'


class ControlFileScanner(object):
    def __init__(self, control_folder_path):
        self.aptio_reagent_info = AptioReagentInfo()
        self.previous_aptio_reagent_info = AptioReagentInfo()
        self.control_file_contents = []
        self.sample_position_info_list = []
        self.sample_flag_info_list = []
        self.position_2_flag_convertor = SamplePosition2FlagStratege()
        self.last_scaned_time_stamp = '0'
        self.control_folder_path = control_folder_path

    def read_control_file_contents(self):
        self.control_file_contents = []
        latest_packed_control_file = GetLatestPackedControlFile(self.control_folder_path).get_latest_packed_control_file()
        try:
            # read packed .xml file first.
            if latest_packed_control_file:
                packed_control_file_handler = open(latest_packed_control_file)
                self.control_file_contents = packed_control_file_handler.readlines()
            # read control.txt file
            control_file = os.path.join(self.control_folder_path, CONTROL_FILE)
            if os.path.isfile(control_file):
                control_file_handler = open(control_file)
                self.control_file_contents += control_file_handler.readlines()

            # reverse control file so that most update
            self.control_file_contents.reverse()
        except Exception as e:
            project_logger.write_log_message(e)
            project_logger.write_log_message("open control file failed!")
        finally:
            if latest_packed_control_file:
                packed_control_file_handler.close()
            if os.path.isfile(control_file):
                control_file_handler.close()


    def scan_control_file_for_position_info(self):
        sample_inlabbing_position_list = []
        self.sample_position_info_list = []
        if self.control_file_contents:
            for line in self.control_file_contents:
                if isinstance(line, str):
                    if line.find("IOM SAMPLE-DETECTED") > 0:
                        info_list = line.split("^")
                        module_id = info_list[0].split(ASCII_SPACE)[5]
                        time_stamp = info_list[0].split(ASCII_SPACE)[1][11:25]
                        if time_stamp > self.last_scaned_time_stamp or self.last_scaned_time_stamp < "1":
                            sample_inlabbing_position_list.append(SampleInlabbingPosition(sample_id=info_list[1],
                                                                                          module_id=module_id,
                                                                                          rack_id=info_list[3],
                                                                                          lane_id=info_list[5],
                                                                                          rack_position=info_list[6],
                                                                                          time_stamp=time_stamp))
        self.sample_position_info_list = sample_inlabbing_position_list
        if sample_inlabbing_position_list:
            self.last_scaned_time_stamp = sample_inlabbing_position_list[0].time_stamp
        return sample_inlabbing_position_list

    def construct_sample_flag_from_position(self):
        self.sample_flag_info_list = []
        for item in self.sample_position_info_list:
            flaged_sample = self.position_2_flag_convertor.position2flag(item)
            if flaged_sample:
                self.sample_flag_info_list.append(flaged_sample)
                # project_logger.write_log_message("flaged sample scanned:" + str(flaged_sample))


    def scan_control_file_for_reagent_info(self):
        if self.control_file_contents:
            for line in self.control_file_contents:
                if line.find('INVENTORY') > 0:
                    inventory_info = line.split(' ')
                    time_stamp = inventory_info[1].split(r'"')[1]
                    instrument_id = inventory_info[4].split(r'"')[1]

                    instrument_reagent_info = self.aptio_reagent_info.get_instrument_inventory_by_id(instrument_id)

                    # if instrument reagent info is found, update its time stamp, otherwise, create a new one.
                    # time stamp is older than current time stamp is ignored.
                    if instrument_reagent_info:
                        if instrument_reagent_info.time_stamp <= time_stamp:
                            instrument_reagent_info.update_time_stamp(time_stamp)
                    else:
                        instrument_type = inventory_info[5]
                        instrument_reagent_info = InstrumentReagentInfo(instr_id=instrument_id, instr_type=instrument_type, time_stamp=time_stamp, reagent_info_list=[])
                        # add instrument reagent inventory into the list.
                        self.aptio_reagent_info.add_aptio_reagent_info_table(instrument_reagent_info)

                    reagent_inventory_info = inventory_info[7]
                    if isinstance(reagent_inventory_info, str):
                        inventory_info_list = reagent_inventory_info.split("\\")
                    for item in inventory_info_list:
                        if item.find("^") > 0:
                            reagent_pair = item.split("^")
                            instrument_reagent_info.update_reagent_info_item(reagent_name=reagent_pair[-3], reagent_count=reagent_pair[-2])

        # update reagent status.
        ReagentStatusUpdateStrategy().update_reagent_status_from_aptio_reagent_info_list(self.aptio_reagent_info)

    def update_previous_aptio_reagent_info(self):
        self.previous_aptio_reagent_info = self.aptio_reagent_info

    def get_reagent_info(self):
        return self.aptio_reagent_info

    def get_inlabbing_info(self):
        return self.sample_flag_info_list

if __name__ == "__main__":
    control_file_folder_path = r'D:\01_Automation\20_Experiential_Conclusions_2015\53_Zhongshan_Aptio\01_Aptio\Log\Logs-150826'
    scanner = ControlFileScanner(control_file_folder_path)
    scanner.read_control_file_contents()
    # sample in-labbing position Processing.
    scanner.scan_control_file_for_position_info()
    scanner.construct_sample_flag_from_position()
    # reagent inventory info processing.
    scanner.scan_control_file_for_reagent_info()

    # testing for sample in-labbing position
    for sample in scanner.sample_position_info_list:
        print sample
    for flaged_sample in scanner.sample_flag_info_list:
        print flaged_sample

    print (r"////////////////////////////////////////////////////////////////////////////////////////////////")
    print      '-----------------------------------Beautiful Split Line--------------------------------'
    print (r"////////////////////////////////////////////////////////////////////////////////////////////////")

    # testing for reagent inventory scanning.
    for instrInfo in scanner.aptio_reagent_info.reagent_info_table:
        if isinstance(instrInfo, InstrumentReagentInfo):
            print("instrument id: %s, instrument type: %s, time stamp: %s" % (instrInfo.instrument_id, instrInfo.instrument_type, instrInfo.time_stamp))
            for reagent in instrInfo.reagent_info_list:
                if isinstance(reagent, ReagentInfoItem):
                    #print("%s,%d %d" % (reagent.reagent_name, reagent.reagent_count, reagent.reagent_status))
                    print reagent

##################################################################################################################
