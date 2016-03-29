HORIZONTAL_TABLE = b'\x09'


class SampleInlabbingPosition(object):
    def __init__(self, sample_id, module_id, rack_id, lane_id, rack_position, time_stamp):
        self.sample_id = sample_id
        self.module_id = module_id
        self.rack_id = rack_id
        self.lane_id = lane_id
        self.rack_position = rack_position
        self.time_stamp = time_stamp

    def __str__(self):
        return "sample id: " + str(self.sample_id) + HORIZONTAL_TABLE +\
                " module id: " + str(self.module_id) + HORIZONTAL_TABLE +\
                " rack id: " + str(self.rack_id) + HORIZONTAL_TABLE +\
                " lane id: " + str(self.lane_id) + HORIZONTAL_TABLE +\
                " rack position: " + str(self.rack_position) + HORIZONTAL_TABLE +\
                " time stamp: " + str(self.time_stamp)

if __name__ == "__main__":
    position1 = SampleInlabbingPosition(123456, 1, 2333, 12, 23, 20151221115948)
    position2 = SampleInlabbingPosition(33445566, 2, 2344, 12, 43, 20160128135311)

    print position1
    print position2

