__author__ = 'Xi Chen'

import tkFileDialog
import sys
from os import listdir
import os
from sklearn.externals import joblib
from Tkinter import *
import struct
import numpy as np

class ReadingRaw(object):
    def __init__(self,file_name):
        self.readings = []
        f = open(file_name, "rb")
        try:
            byte = f.read(4*1024)
            while byte != "":
                number_vec = struct.unpack('1024f', byte)
                self.readings.append(np.asarray(number_vec))
                byte = f.read(4*1024)
        finally:
            f.close()

if __name__ == "__main__":

    num_cls = 3

    root = Tk()
    root.withdraw()

    file_opt_model = options = {}
    options['filetypes'] = [("pkl files","*.pkl")]
    options['title'] = 'Please choose the model file.'
    options['initialdir'] = os.path.expanduser('~') + '/fm_location'
    file_name_model = tkFileDialog.askopenfilename(**file_opt_model)
    if len(file_name_model)==0:
        print "No model is chosen.\n"
        sys.exit(1)
    clf = joblib.load(file_name_model)
    print "Model loaded successfully"

    file_opt_data = options = {}
    options['filetypes'] = [("data files","*.dat")]
    options['title'] = 'Please choose the offline testing file.'
    options['initialdir'] = os.path.expanduser('~') + '/fm_location'
    file_name_data = tkFileDialog.askopenfilename(**file_opt_data)
    if len(file_name_data)==0:
        print "No testing data is chosen."
        sys.exit(1)
    testing_data = ReadingRaw(file_name_data).readings
    if len(testing_data)>0:
        print "Testing data loaded successfully\n"
        print "There are " + str(len(testing_data)) + " samples in the testing file.\n"

    predict_results = clf.predict(testing_data)
    # predict_perc = np.histogram(predict_results,3,range=(0,2))
    predict_perc = np.zeros(num_cls)
    for i in xrange(num_cls):
        predict_perc[i] = list(predict_results).count(i)
    total_occur = float(sum(predict_perc))
    for i in xrange(num_cls):
        predict_perc[i] = float(predict_perc[i])/total_occur
    print predict_perc
