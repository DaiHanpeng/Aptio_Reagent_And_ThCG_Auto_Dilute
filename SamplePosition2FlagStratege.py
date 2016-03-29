import ConfigParser

from SampleInlabbingPosition import SampleInlabbingPosition
from SampleFlagInfo import SampleFlagInfo

CONVERSION_PARAMETER_INI_FILE = "Parameters.CFG"
SECTION_NAME = "Position2Flag"
RACK_ID = "Rack_Id"
COLUMN_A = "Column_A_Flag"
COLUMN_B = "Column_B_Flag"
COLUMN_C = "Column_C_Flag"
COLUMN_D = "Column_D_Flag"


class SamplePosition2FlagStratege(object):
    def __init__(self):
        self._racks = []
        self._column_a_flag = None
        self._column_b_flag = None
        self._column_c_flag = None
        self._column_d_flag = None
        self.load_configuration_from_file()

    def load_configuration_from_file(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(CONVERSION_PARAMETER_INI_FILE)
        if config_parser.has_section(SECTION_NAME):
            racks = config_parser.get(SECTION_NAME,RACK_ID)
            racks = racks.split(',')
            for rack in racks:
                self._racks.append(rack)
            self._column_a_flag = config_parser.get(SECTION_NAME,COLUMN_A)
            self._column_b_flag = config_parser.get(SECTION_NAME,COLUMN_B)
            self._column_c_flag = config_parser.get(SECTION_NAME,COLUMN_C)
            self._column_d_flag = config_parser.get(SECTION_NAME,COLUMN_D)

    def position2flag(self, sample_position_info):
        if isinstance(sample_position_info, SampleInlabbingPosition):
            rack_matched = False
            for rack in self._racks:
                if str(sample_position_info.rack_id) == rack:
                    rack_matched = True
            if rack_matched:
                column_flag = ''
                rack_position = int(sample_position_info.rack_position)
                if 0 < rack_position <= 12:
                    column_flag = self._column_a_flag
                elif 13<= rack_position <= 24:
                    column_flag = self._column_b_flag
                elif 25<= rack_position <= 36:
                    column_flag = self._column_c_flag
                elif 37<= rack_position <= 48:
                    column_flag = self._column_d_flag
                return SampleFlagInfo(sample_id=sample_position_info.sample_id, flag=column_flag, time_stamp=sample_position_info.time_stamp)
            else:
                return None


if __name__ == "__main__":
    convertor = SamplePosition2FlagStratege()
    position1 = SampleInlabbingPosition(123456, 1, 1234, 12, 21, 20151221115948)
    position2 = SampleInlabbingPosition(33445566, 2, 2344, 12, 43, 20160128135311)
    flag = convertor.position2flag(position1)
    if flag:
        print flag
    flag = convertor.position2flag(position2)
    if flag:
        print flag
