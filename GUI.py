"""
GUI Module and class for adb_runApps_GUI_multithread_v1.py
Runs android apps (Webpages/Ping/Youtube/FTP/PhoneCall)
12/20/2017 - Webpage and Ping only implemented
Authored by Aashish
"""
import datetime
import time
import os
from tkinter import *
from queue import *
import threading
from tkinter import ttk
import collections
import re

class GUI:
    def __init__(self, master, adb_choices):
        #Variables
        #self.widgets = ['Website','Youtube','Ping']
        self.apps = ['Website','Ping','Youtube']
        self.allApps = collections.defaultdict()
        self.apps_label = ['Website','Ping','Youtube']
        self.apps_addresstext =['','127.0.0.1','']
        self.apps_time = [30,40,50]
        self.apps_freq = [2,1,'']
        self.apps_chkbox = [1,0,0]
        self.apps_status=['normal','normal','disabled']

        self.activity = ""

        self.master = master
        self.adb_choices = adb_choices

        r=0
        self.varADB = StringVar()
        self.varADBchoice = StringVar()
        Label(self.master, textvariable=self.varADB, font='Helvetica 12', relief=SUNKEN).grid(row=r,column=0)
        self.varADB.set("Device")
        OptionMenu(self.master, self.varADBchoice, *self.adb_choices).grid(row=r, column=1, padx=5, pady=5)
        self.varADBchoice.set(list(self.adb_choices)[1])

        r = r + 25
        self.varAppTitle = StringVar()
        self.varAddressTitle = StringVar()
        self.varTimeTitle = StringVar()
        self.varFreqTitle = StringVar()
        self.varAskTitle = StringVar()
        Label(self.master, textvariable=self.varAppTitle, font='Helvetica 12 bold', relief=RIDGE).grid(row=r,column=0)
        Label(self.master, textvariable=self.varAddressTitle, font='Helvetica 12 bold', relief=RIDGE).grid(row=r,column=1)
        Label(self.master, textvariable=self.varTimeTitle, font='Helvetica 12 bold', relief=RIDGE).grid(row=r,column=2)
        Label(self.master, textvariable=self.varFreqTitle, font='Helvetica 12 bold', relief=RIDGE).grid(row=r,column=3)
        Label(self.master, textvariable=self.varAskTitle, font='Helvetica 12 bold', relief=RIDGE).grid(row=r,column=4)
        self.varAppTitle.set("App Name")
        self.varAddressTitle.set("Adress/IP")
        self.varTimeTitle.set("Total Time(min)")
        self.varFreqTitle.set("Frequency(sec)")
        self.varAskTitle.set("En/Dis")

        print(self.apps_addresstext[0])

        r = r + 20

        for widgetIdx, appsKeyName in enumerate(self.apps):
            self.allApps[appsKeyName] = collections.defaultdict()
            self.allApps[appsKeyName]['LabelText'] = StringVar()
            self.allApps[appsKeyName]['AddressText'] = StringVar()
            self.allApps[appsKeyName]['TimeText'] = IntVar()
            self.allApps[appsKeyName]['FreqText'] = IntVar()
            self.allApps[appsKeyName]['CheckedInt'] = IntVar()
            self.allApps[appsKeyName]['EnabledInt'] = StringVar()

            # config(state = DISABLED)
            self.allApps[appsKeyName]['LabelWidget'] = Label(self.master, textvariable=self.allApps[appsKeyName]['LabelText'], justify = CENTER, state=self.apps_status[widgetIdx], relief=SUNKEN)
            self.allApps[appsKeyName]['LabelWidget'].grid(row=r,column=0,padx=5, pady=5)
            self.allApps[appsKeyName]['LabelText'].set(self.apps_label[widgetIdx])
            if appsKeyName is 'Website':
                #self.widget_text[widgetIdx]='wikilinks'
                choices = { 'wikilinks','http://www.time.com','http://www.nfl.com','http://www.cnn.com'}
                self.allApps[appsKeyName]['AddressWidget'] = OptionMenu(self.master, self.allApps[appsKeyName]['AddressText'], *choices)
                self.allApps[appsKeyName]['AddressText'].set("wikilinks")
            else:
                self.allApps[appsKeyName]['AddressWidget'] = Entry(self.master, textvariable=self.allApps[appsKeyName]['AddressText'], justify = CENTER, state=self.apps_status[widgetIdx])
                self.allApps[appsKeyName]['AddressText'].set(self.apps_addresstext[widgetIdx])
            self.allApps[appsKeyName]['AddressWidget'].grid(row=r, column=1, padx=5, pady=5)
            # print(self.apps_addresstext[widgetIdx])

            self.allApps[appsKeyName]['TimeWidget'] = Entry(self.master, textvariable=self.allApps[appsKeyName]['TimeText'], justify = CENTER, state=self.apps_status[widgetIdx])
            self.allApps[appsKeyName]['TimeWidget'].grid(row=r, column=2, padx=5, pady=5)
            self.allApps[appsKeyName]['TimeText'].set(self.apps_time[widgetIdx])
            self.allApps[appsKeyName]['FreqWidget'] = Entry(self.master, textvariable=self.allApps[appsKeyName]['FreqText'], justify = CENTER, state=self.apps_status[widgetIdx])
            self.allApps[appsKeyName]['FreqWidget'].grid(row=r, column=3, padx=5, pady=5)
            self.allApps[appsKeyName]['FreqText'].set(self.apps_freq[widgetIdx])
            if appsKeyName is "Website":
                self.allApps[appsKeyName]['CheckedWidget'] = Checkbutton(self.master, text="", variable=self.allApps[appsKeyName]['CheckedInt'], state=self.apps_status[widgetIdx], command=lambda:self.chk_web())
            if appsKeyName is "Ping":
                self.allApps[appsKeyName]['CheckedWidget'] = Checkbutton(self.master, text="", variable=self.allApps[appsKeyName]['CheckedInt'], state=self.apps_status[widgetIdx], command=lambda:self.chk_ping())
            if appsKeyName is "Youtube":
                self.allApps[appsKeyName]['CheckedWidget'] = Checkbutton(self.master, text="", variable=self.allApps[appsKeyName]['CheckedInt'], state=self.apps_status[widgetIdx], command=lambda:self.chk_youtube())
            self.allApps[appsKeyName]['CheckedWidget'].grid(row=r, column=4, padx=5, pady=5)
            self.allApps[appsKeyName]['CheckedInt'].set(self.apps_chkbox[widgetIdx])
            r = r + 1
            r = r + 10
            self.btnSubmit = Button(self.master, text="Go For It!", command=self.submit)
            self.btnSubmit.grid(row=r, column=1)
            self.btnClose = Button(self.master, text="Close", justify=RIGHT,command=self.close_button)
            self.btnClose.grid(row=r, column=2)
            self.btnClose = Button(self.master, text="Stop", justify=RIGHT,command=self.stop_all_process)
            self.btnClose.grid(row=r, column=3)

    def chk_web(self):
        if self.allApps["Website"]['CheckedInt'].get():
            self.allApps["Ping"]['CheckedInt'].set(0)
            self.allApps["Youtube"]['CheckedInt'].set(0)

    def chk_ping(self):
        if self.allApps["Ping"]['CheckedInt'].get():
            self.allApps["Website"]['CheckedInt'].set(0)
            self.allApps["Youtube"]['CheckedInt'].set(0)

    def chk_youtube(self):
        if self.allApps["Youtube"]['CheckedInt'].get():
            self.allApps["Website"]['CheckedInt'].set(0)
            self.allApps["Ping"]['CheckedInt'].set(0)

    def close_button(self):
        #print("Inside Close button")
        try:
            self.queue.put("Stop")
        except:
            pass
        #print("Queue putting Stop from Close button. Exiting now")
        time.sleep(1)
        self.master.quit()


    def stop_all_process(self):
        print("Inside Stop button")
        try:
            self.queue.put("Stop")
        except:
            pass
        time.sleep(1)
        for widgetIdx, appsKeyName in enumerate(self.apps):
            self.allApps[appsKeyName]['LabelWidget'].config(state=self.apps_status[widgetIdx])
            self.allApps[appsKeyName]['AddressWidget'].config(state=self.apps_status[widgetIdx])
            self.allApps[appsKeyName]['TimeWidget'].config(state=self.apps_status[widgetIdx])
            self.allApps[appsKeyName]['FreqWidget'].config(state=self.apps_status[widgetIdx])
            self.allApps[appsKeyName]['CheckedWidget'].config(state=self.apps_status[widgetIdx])

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            print("Process_queue msg" +msg)
            # Show result of the task if needed
            if msg in "Stop":
                print(msg)
                #self.master.destroy()
        except Empty:
            #print("The queue is empty -- printed from process_queue")
            self.master.after(100, self.process_queue)

    def submit(self):
    	#checkbutton variable type is integer (not str or bool)
        for widgetIdx, appsKeyName in enumerate(self.apps):
            self.allApps[appsKeyName]['LabelWidget'].config(state=DISABLED)
            self.allApps[appsKeyName]['AddressWidget'].config(state=DISABLED)
            self.allApps[appsKeyName]['TimeWidget'].config(state=DISABLED)
            self.allApps[appsKeyName]['FreqWidget'].config(state=DISABLED)
            self.allApps[appsKeyName]['CheckedWidget'].config(state=DISABLED)
            if appsKeyName in "Website":
                if self.allApps[appsKeyName]['CheckedInt'].get() and self.allApps[appsKeyName]['TimeText'].get() > 0 and self.allApps[appsKeyName]['FreqText'].get() > 0:
                    print("Running website " + self.allApps[appsKeyName]['AddressText'].get() +" for "+str(self.allApps[appsKeyName]['TimeText'].get()))
                    self.queue = Queue()
                    self.activity = "browsing"
                    ThreadedTask(self.queue, self.activity, self.allApps[appsKeyName]['AddressText'].get(), self.allApps[appsKeyName]['TimeText'].get(), self.allApps[appsKeyName]['FreqText'].get()).start()
                    # self.master.after(100, self.process_queue)
            if appsKeyName in "Ping":
                if self.allApps[appsKeyName]['CheckedInt'].get() and self.allApps[appsKeyName]['TimeText'].get() > 0 and self.allApps[appsKeyName]['FreqText'].get() > 0:
                    print("Pinging IP Address " + self.allApps[appsKeyName]['AddressText'].get() +" for "+str(self.allApps[appsKeyName]['TimeText'].get()))
                    self.queue = Queue()
                    self.activity = "pinging"
                    ThreadedTask(self.queue, self.activity, self.allApps[appsKeyName]['AddressText'].get(), self.allApps[appsKeyName]['TimeText'].get(), self.allApps[appsKeyName]['FreqText'].get()).start()
                #Run Youtube here
            if appsKeyName in "Youtube":
                pass
                #Run Ping here

class ThreadedTask(threading.Thread):
    def __init__(self, queue, activity, address, time, freq):
        threading.Thread.__init__(self)
        self.queue = queue
        self.activity = activity
        self.address = address
        self.time = time
        self.freq = freq
        self.websites_lists =["https://en.m.wikipedia.org/wiki/" + str(i) for i in range (1850,1880)]

    def run_webpages(webpage):
        print(print_timestamp() + " " + "---Browsing " + webpage)
        start_webpage_command = "adb shell am start -a android.intent.action.VIEW -d " + webpage
        os.system(start_webpage_command)

    def run(self):
        #time.sleep(5)
        #Simulate long running process
        if self.activity in "browsing":
            timestart = datetime.datetime.now()
            print(str(timestart) + "--Waiting for device")
            os.system("adb wait-for-device devices")

            timesince = datetime.datetime.now() - timestart
            minutessince = int(timesince.total_seconds()/60)
            secondsince = int(timesince.total_seconds())
            runactivity = True
            while(minutessince < self.time and runactivity):
                if self.address in "wikilinks":
                    for webpage in self.websites_lists:
                        #print("minutessince ="+str(minutessince) + "and runactivity="+str(runactivity))
                        start_webpage_command = "adb shell am start -a android.intent.action.VIEW -d " + webpage
                        os.system(start_webpage_command)
                        print("Browsing " + webpage)
                        time.sleep(self.freq)
                        try:
                            msg = self.queue.get(0)
                            #IMP Print
                            #print("msg after close or stop = " + msg + "--printed from webloop")
                            if msg in "Stop":
                                runactivity = False
                                break
                        except:
                            #IMP Print
                            #print("Queue looks empty. Didn't extract anything")
                            pass
                else:
                    start_webpage_command = "adb shell am start -a android.intent.action.VIEW -d " + str(self.address)
                    os.system(start_webpage_command)
                    time.sleep(self.freq)
                    try:
                        msg = self.queue.get(0)
                        #IMP Print
                        #print("msg after close = " + msg + "--printed from webloop")
                        if msg in "Stop":
                            runactivity = False
                            break
                    except:
                        #IMP Print
                        #print("Queue looks empty. Didn't extract anything")
                        pass
        elif self.activity in "pinging":
            # Windows ping doesnt have interval. Ping max size 65500
            # ADB ping w interval 4sec, size 4200 bytes => ping -i 4 -s 4200 10.73.9.48
            timestart = datetime.datetime.now()
            print(str(timestart) + "--Waiting for device")
            os.system("adb wait-for-device devices")

            timesince = datetime.datetime.now() - timestart
            minutessince = int(timesince.total_seconds()/60)
            secondsince = int(timesince.total_seconds())
            runactivity = True
            size_in_byte = 128
            ip_pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
            if re.search(ip_pattern, self.address):
                while(minutessince < self.time and runactivity):
                #matchObject = re.search(pattern, input_str, flags=0)
                    print("Pinging " + self.address)
                    start_ping_command = "adb shell ping -c 1 -s " + str(size_in_byte) + " " + str(self.address)
                    time.sleep(self.freq)
                    print("start_ping_command="+start_ping_command)
                    os.system(start_ping_command)
                    try:
                        msg = self.queue.get(0)
                        #print("msg after close or stop = " + msg + "--printed from webloop")
                        if msg in "Stop":
                            runactivity = False
                            break
                    except:
                        pass
            else:
                print("IP Address doesnt match the format")
