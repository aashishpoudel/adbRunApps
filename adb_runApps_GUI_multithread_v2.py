"""
Runs android apps (Webpages/Ping/Youtube/FTP/PhoneCall)
v2 - Webpage and Ping only implemented
Authored by Aashish
"""

import subprocess
import time
import os
import collections
from tkinter import *
from subprocess import check_output
import signal
import sys
from GUI import *

def print_timestamp():
	return datetime.datetime.now().strftime('%Y-%m-%d.%H%M%S')

"""
List of devices attached
321d9a9a	device

>>> from subprocess import check_output
>>> adb_output = check_output(["adb","devices"])
>>> adb_output
b'List of devices attached \n321d9a9a\tdevice\n\n'

replacements = ('\\n', '\\t', 'b\'')
adb_output_str = str(adb_output)
for r in replacements:
    adb_output_str = adb_output_str.replace(r, ' ')

words = adb_output_str.split()
>>> words
['List', 'of', 'devices', 'attached', '321d9a9a', 'device', "'"]


"""

#https://en.m.wikipedia.org/wiki/1945
websites_lists =["https://en.m.wikipedia.org/wiki/" + str(i) for i in range (1850,2017)]

sleep_duration = 2
total_duration_in_min = 30

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

window=Tk()

adb_output = check_output(["adb","devices"])
#adb_output =b'List of devices attached \n321d9a9a\tdevice\n\n'
replacements = ('\\n', '\\t', 'b\'')
adb_output_str = str(adb_output)
for r in replacements:
    adb_output_str = adb_output_str.replace(r, ' ')
adb_output_str_split = adb_output_str.split()
#>>> adb_output_str_split = ['List', 'of', 'devices', 'attached', '321d9a9a', 'device', "'"]
adb_choices = {adb_output_str_split[4],'dummy'}
print(str(adb_choices))

window.title("Run ADB Tests")
main_ui = GUI(window, adb_choices)

window.mainloop()
