__author__ = 'Xi Chen'

import subprocess
import os
import time
import sys
import tkSimpleDialog
import Tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    file_name = tkSimpleDialog.askstring(title='Name of the record', prompt='Enter here: ')
    if file_name is None:
        sys.exit(0)
    measure_time = tkSimpleDialog.askfloat(title='Duration in seconds', prompt='Enter here: ')
    if measure_time is None:
        sys.exit(0)

    time.sleep(0.5)
    # home_path = os.path.expanduser('~')
    os.chdir(os.getcwd()+'/grc/')
    cmd_str = '--command=python fm_recv.py ' + file_name
    subprocess.Popen(['gnome-terminal', cmd_str])
    time.sleep(measure_time+2)
    os.system("sudo pkill python")
