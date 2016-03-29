__author__ = 'Z003CA1K'

# defiend as Reagent status
UNKNOWN = 0
GREEN = 1
YELLOW = 2
RED = 3

reagent_status_map = {UNKNOWN:'Unknown',GREEN:'Green',YELLOW:'Yellow',RED:'Red'}

HORIZONTAL_TABLE = b'\x09'


class ReagentInfoItem(object):
    '''
    This class if defined for a single reagent info unit, from the table's view, its a cell of the table.
    '''
    def __init__(self, name, count, pre_status=GREEN, status=GREEN):
        self.reagent_name = name
        self.reagent_count = count
        self.pre_reagent_status = pre_status
        self.reagent_status = status

    def __str__(self):
        return 'reagent name: ' + self.reagent_name + HORIZONTAL_TABLE +\
               'reagent count: ' + str(self.reagent_count) + HORIZONTAL_TABLE +\
               'previous reagent status: ' + reagent_status_map[self.pre_reagent_status] + HORIZONTAL_TABLE +\
               'reagent status: ' + reagent_status_map[self.reagent_status]


class InstrumentReagentInfo(object):
    '''
    This class is defined for single instrument,from the table's view, its a column of the reagent info table.
    '''
    def __init__(self, instr_id, instr_type, time_stamp=None, reagent_info_list=[]):
        '''
        Instrument_Id: str
        Instrument_Type: str
        Reagent_Info_List: ReagentInfoItem[]
        '''
        self.instrument_id = instr_id
        self.instrument_type = instr_type
        self.time_stamp = time_stamp
        self.reagent_info_list = reagent_info_list

    def add_reagent_info_item(self, reagent_info_item):
        if isinstance(reagent_info_item, ReagentInfoItem):
            self.reagent_info_list.append(reagent_info_item)

    def update_time_stamp(self, time_stamp):
        self.time_stamp = time_stamp

    def update_reagent_info_item(self, reagent_name, reagent_count):
        reagent_info = self.get_reagent_info_item_by_reagent_name(reagent_name)
        if reagent_info:
            reagent_info.reagent_count = reagent_count
        else:
            self.add_reagent_info_item(ReagentInfoItem(name=reagent_name,count=reagent_count))

    def get_reagent_info_item_by_reagent_name(self, name):
        for item in self.reagent_info_list:
            if isinstance(item, ReagentInfoItem):
                if item.reagent_name == name:
                    return item
        return None


    def clear_reagent_info_items(self):
        self.reagent_info_list = []

class AptioReagentInfo(object):
    '''
    This class is defined for the whole reagent info table.
    '''
    def __init__(self):
        self.reagent_info_table = []

    def add_aptio_reagent_info_table(self, instr_reagent_info):
        if isinstance(instr_reagent_info, InstrumentReagentInfo):
            self.reagent_info_table.append(instr_reagent_info)

    def clear_aptio_reagentr_info_table(self):
        self.reagent_info_table = []

    def get_instrument_inventory_by_id(self, instrument_id):
        for instrument in self.reagent_info_table:
            if isinstance(instrument, InstrumentReagentInfo):
                if instrument_id == instrument.instrument_id:
                    return instrument
        return None



######################################################################################################################################################
# Module Test Section
######################################################################################################################################################
if __name__ == "__main__":
    '''
    let's test it below...
    '''
    # construct some Reagent Cells
    ReagentInfoItem11 = ReagentInfoItem('dai', 12, GREEN,RED)
    ReagentInfoItem12 = ReagentInfoItem('han', 13, YELLOW,RED)
    ReagentInfoItem13 = ReagentInfoItem('peng', 14, RED,YELLOW)
    ReagentInfoList1 = [ReagentInfoItem11, ReagentInfoItem12, ReagentInfoItem13]

    ReagentInfoItem21 = ReagentInfoItem('I', 32, GREEN,GREEN)
    ReagentInfoItem22 = ReagentInfoItem('love', 33, GREEN,RED)
    ReagentInfoItem23 = ReagentInfoItem('python', 34, GREEN,YELLOW)
    ReagentInfoList2 = [ReagentInfoItem21, ReagentInfoItem22, ReagentInfoItem23]

    # Construct some Instrument Reagent Info
    InstrumentInfo1 = InstrumentReagentInfo(5, 'A24', '20160101110909', ReagentInfoList1)
    InstrumentInfo2 = InstrumentReagentInfo(7, 'CEN', '20151212090923', ReagentInfoList2)

    # Construct An Aptio Reagent Info Table
    aptioReagentInfo = AptioReagentInfo()
    aptioReagentInfo.add_aptio_reagent_info_table(InstrumentInfo1)
    aptioReagentInfo.add_aptio_reagent_info_table(InstrumentInfo2)

    # show all the messages...
    for instrInfo in aptioReagentInfo.reagent_info_table:
        if isinstance(instrInfo, InstrumentReagentInfo):
            print("intstrument id:%i,instrument type:%s,time stamp:%s" % (instrInfo.instrument_id, instrInfo.instrument_type, instrInfo.time_stamp))
            for reagent in instrInfo.reagent_info_list:
                if isinstance(reagent, ReagentInfoItem):
                    #print("%s,%d %d" % (reagent.reagent_name, reagent.reagent_count, reagent.reagent_status))
                    print reagent
