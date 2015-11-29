__author__ = 'Xi Chen'

import scipy.io as sio
from os import listdir
from sklearn.svm import SVC
from sklearn import tree
from sklearn import decomposition
from sklearn.externals import joblib
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from Tkinter import *
import tkFileDialog
import struct
import numpy as np
import os

class ReadingRaw(object):
    def __init__(self,file_name,index):
        self.readings = []
        self.labels = []
        f = open(file_name, "rb")
        try:
            byte = f.read(4*1024)
            while byte != "":
                number_vec = struct.unpack('1024f', byte)
                self.readings.append(np.asarray(number_vec))
                self.labels.append(index)
                byte = f.read(4*1024)
        finally:
            f.close()

if __name__ == "__main__":

    xvalid = False

    root = Tk()
    root.withdraw()

    folder_name = tkFileDialog.askdirectory(title='Please choose the directory of training files.') + '/'
    if len(folder_name)==1:
        print "No file is chosen."
        sys.exit(0)
    file_names = [ folder_name+f for f in listdir(folder_name) if f.endswith('.dat') ]
    file_names = sorted(file_names)
    print file_names

    all_readings = []
    all_labels = []
    num_repeats = 3
    for index_file in xrange(len(file_names)):
        cur_reading_ins = ReadingRaw(file_names[index_file],index_file/num_repeats)
        tmp_reading = cur_reading_ins.readings
        all_readings = all_readings + tmp_reading
        # all_readings.append(tmp_reading)
        tmp_label = cur_reading_ins.labels
        all_labels = all_labels + tmp_label
        # all_labels.append(tmp_label)
        print np.shape(tmp_reading)
        print np.shape(tmp_label)
    print np.shape(all_readings)
    print np.shape(all_labels)

    if xvalid:
        test_clf = SVC(kernel='linear', C=1.0)
        scroes_SVM = cross_val_score(test_clf,all_readings,all_labels)
        print 'SVM: ' + str(scroes_SVM.mean()),
        print '    ' + str(np.power(scroes_SVM.std(),2))

        test_clf = RandomForestClassifier(n_estimators=100)
        scroes_randomforest = cross_val_score(test_clf,all_readings,all_labels)
        print 'Random Forest: ' + str(scroes_randomforest.mean()),
        print '    ' + str(np.power(scroes_randomforest.std(),2))

    save_folder_svm = folder_name + 'SVM_model/'
    save_folder_RF = folder_name + 'RF_model/'
    if not os.path.exists(save_folder_svm):
        os.makedirs(save_folder_svm)
    if not os.path.exists(save_folder_RF):
        os.makedirs(save_folder_RF)

    clf_SVM = SVC(kernel='linear', C=1.0)
    clf_SVM.fit(all_readings,all_labels)
    joblib.dump(clf_SVM,save_folder_svm+'SVM.pkl')

    clf_RF = RandomForestClassifier(n_estimators=100)
    clf_RF.fit(all_readings,all_labels)
    joblib.dump(clf_RF,save_folder_RF+'RF.pkl')
