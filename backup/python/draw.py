__author__ = "Xi Chen"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import read_raw

class test(object):
    def __init__(self, readings):
        self.readings = readings

if __name__ == "__main__":
    from_input = read_raw.ReadingRaw()
    all_samples = from_input.readings
    print np.shape(all_samples)