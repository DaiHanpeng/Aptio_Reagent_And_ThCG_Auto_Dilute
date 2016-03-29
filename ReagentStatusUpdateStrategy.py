import ConfigParser
from Aptio_Reagent_Info import AptioReagentInfo, InstrumentReagentInfo,ReagentInfoItem
from Aptio_Reagent_Info import *

HORIZONTAL_TABLE = b'\x09'
REAGENT_STATUS_THRESHOLD_CONFIG_FILE = 'Reagent Status Threshold.CFG'
REAGENT_STATUS_THRESHOLD_SECTION_NAME = 'Reagent Status Threshold'

class ReagentStatusThreshold(object):
    def __init__(self, reagent_name, yellow_threshold=100, red_threshold=10):
        self.reagent_name = reagent_name
        self.yellow_threshold = yellow_threshold
        self.red_threshold = red_threshold

    def __str__(self):
        return 'reagent name: ' + self.reagent_name + HORIZONTAL_TABLE + \
               'yellow threshold: ' + str(self.yellow_threshold) + HORIZONTAL_TABLE +\
                'red threshold: ' + str(self.red_threshold)


class AptioReagentStatusThreshold(object):
    def __init__(self):
        self.reagent_status_threshold_list = []

    def add_reagent_item(self, reagent_item):
        if isinstance(reagent_item, ReagentStatusThreshold):
            self.reagent_status_threshold_list.append(reagent_item)

    def build_reagent_status_thresholds_from_config_file(self, config_file=REAGENT_STATUS_THRESHOLD_CONFIG_FILE):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)
        if config_parser.has_section(REAGENT_STATUS_THRESHOLD_SECTION_NAME):
            reagent_status_threshold_items = config_parser.items(REAGENT_STATUS_THRESHOLD_SECTION_NAME)
        for item in reagent_status_threshold_items:
            yellow_threshold = int(item[1].split(',')[0])
            red_threshold = int(item[1].split(',')[1])
            threshold_item = ReagentStatusThreshold(reagent_name=item[0],yellow_threshold=yellow_threshold,red_threshold=red_threshold)
            self.add_reagent_item(threshold_item)

    def get_reagent_status_threshold_list(self):
        return self.reagent_status_threshold_list

class ReagentStatusUpdateStrategy(object):
    def __init__(self):
        aptio_reagent_status_threshold = AptioReagentStatusThreshold()
        aptio_reagent_status_threshold.build_reagent_status_thresholds_from_config_file()
        self.reagent_status_threshold_list = aptio_reagent_status_threshold.get_reagent_status_threshold_list()

    def update_reagent_status_from_aptio_reagent_info_list(self, aptio_reagent_info):
        if isinstance(aptio_reagent_info, AptioReagentInfo):
            for instrument in aptio_reagent_info.reagent_info_table:
                if isinstance(instrument, InstrumentReagentInfo):
                    for reagent_item in instrument.reagent_info_list:
                        self.update_reagent_status_from_reagent_item(reagent_item)

    def update_reagent_status_from_reagent_item(self, reagent_item):
        if isinstance(reagent_item, ReagentInfoItem):
            for item in self.reagent_status_threshold_list:
                if isinstance(item, ReagentStatusThreshold):
                    if isinstance(item.reagent_name,str) and isinstance(reagent_item.reagent_name,str):
                        if item.reagent_name.lower() == reagent_item.reagent_name.lower():
                            # update previous reagent status.
                            reagent_item.pre_reagent_status = reagent_item.reagent_status
                            # update current reagent status.
                            if int(reagent_item.reagent_count) <= int(item.red_threshold):
                                reagent_item.reagent_status = RED
                            elif int(reagent_item.reagent_count) <= int(item.yellow_threshold):
                                reagent_item.reagent_status = YELLOW
                            else:
                                reagent_item.reagent_status = GREEN

if __name__ == '__main__':
    aptio_reagent_status_threshold = AptioReagentStatusThreshold()
    aptio_reagent_status_threshold.build_reagent_status_thresholds_from_config_file()
    threshold_list = aptio_reagent_status_threshold.get_reagent_status_threshold_list()
    for item in threshold_list:
        print item

    print r'///////////////////////////////////////////////////////////////////////////'

    # construct some Reagent Cells
    ReagentInfoItem11 = ReagentInfoItem('dai', 12, GREEN)
    ReagentInfoItem12 = ReagentInfoItem('han', 13, GREEN)
    ReagentInfoItem13 = ReagentInfoItem('peng', 14, GREEN)
    ReagentInfoList1 = [ReagentInfoItem11, ReagentInfoItem12, ReagentInfoItem13]

    ReagentInfoItem21 = ReagentInfoItem('I', 32, GREEN)
    ReagentInfoItem22 = ReagentInfoItem('love', 33, GREEN)
    ReagentInfoItem23 = ReagentInfoItem('python', 34, GREEN)
    ReagentInfoList2 = [ReagentInfoItem21, ReagentInfoItem22, ReagentInfoItem23]

    # Construct some Instrument Reagent Info
    InstrumentInfo1 = InstrumentReagentInfo(5, 'A24', ReagentInfoList1)
    InstrumentInfo2 = InstrumentReagentInfo(7, 'CEN', ReagentInfoList2)

    # Construct An Aptio Reagent Info Table
    aptioReagentInfo = AptioReagentInfo()
    aptioReagentInfo.add_aptio_reagent_info_table(InstrumentInfo1)
    aptioReagentInfo.add_aptio_reagent_info_table(InstrumentInfo2)

    # update reagent status.
    ReagentStatusUpdateStrategy().update_reagent_status_from_aptio_reagent_info_list(aptioReagentInfo)

    # show all the messages...
    for instrInfo in aptioReagentInfo.reagent_info_table:
        if isinstance(instrInfo, InstrumentReagentInfo):
            print("%i,%s" % (instrInfo.instrument_id, instrInfo.instrument_type))
            for reagent in instrInfo.reagent_info_list:
                if isinstance(reagent, ReagentInfoItem):
                    #print("%s,%d %d" % (reagent.reagent_name, reagent.reagent_count, reagent.reagent_status))
                    print reagent
