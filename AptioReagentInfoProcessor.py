from Aptio_Reagent_Info import *

class AptioReagentInfoProcessor(object):
    def __init__(self, aptio_reagent_info):
        if isinstance(aptio_reagent_info, AptioReagentInfo):
            self.aptio_reagent_info = aptio_reagent_info

    def process(self):
        self.send_reagent_enable_disable_message()
        self.show_enable_disable_message()

    def send_reagent_enable_disable_message(self):
        pass

    def show_enable_disable_message(self):
        for instrInfo in self.aptio_reagent_info.reagent_info_table:
            if isinstance(instrInfo, InstrumentReagentInfo):
                for reagent_item in instrInfo.reagent_info_list:
                    if isinstance(reagent_item, ReagentInfoItem):
                        if reagent_item.pre_reagent_status <> RED and reagent_item.reagent_status == RED:
                            print(reagent_item.reagent_name + ' disabled')
                        if reagent_item.pre_reagent_status <> GREEN and reagent_item.reagent_status == GREEN:
                            print(reagent_item.reagent_name + ' enabled')

if __name__ == '__main__':
    # construct some Reagent Cells
    ReagentInfoItem11 = ReagentInfoItem('dai', 12, GREEN,RED)
    ReagentInfoItem12 = ReagentInfoItem('han', 13, YELLOW,RED)
    ReagentInfoItem13 = ReagentInfoItem('peng', 14, RED,YELLOW)
    ReagentInfoList1 = [ReagentInfoItem11, ReagentInfoItem12, ReagentInfoItem13]

    ReagentInfoItem21 = ReagentInfoItem('I', 32, RED,GREEN)
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

    AptioReagentInfoProcessor(aptioReagentInfo).process()