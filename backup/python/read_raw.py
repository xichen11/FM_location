__author__ = "Xi Chen"

import struct
import numpy as np


class ReadingRaw(object):
    def __init__(self):
        self.readings = []
        f = open("raw", "rb")
        try:
            byte = f.read(4*1024)
            while byte != "":
                number_vec = struct.unpack('1024f', byte)
                self.readings.append(np.asarray(number_vec))
                byte = f.read(4*1024)
        finally:
            f.close()

