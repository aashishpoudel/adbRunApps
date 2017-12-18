import datetime
import time
import os
from tkinter import *
from queue import *
import threading
from tkinter import ttk

class GUI:
    def __init__(self, master, adb_choices):
        #Variables
        self.widgets = ['Website','Youtube','Ping']
        self.myWidgets = [dict() for i in range(len(self.widgets))]

        self.widgets_label = ['Website','Youtube','Ping']
        self.widget_text =['','','']
        self.widget_time = [30,40,50]
        self.widget_chkbox = [1,0,0]
        self.widget_status=['normal','disabled','disabled']

        self.activity = ""

        self.master = master
        self.adb_choices = adb_choices
        r=0
        self.varADB = StringVar()
        self.varADBchoice = StringVar()
        Label(self.master, textvariable=self.varADB, font='Helvetica 15 bold', relief=SUNKEN).grid(row=r,column=0)
        OptionMenu(self.master, self.varADBchoice, *self.adb_choices).grid(row=r, column=1, padx=5, pady=5)
        self.varADBchoice.set("mydevice")
        # self.varADBchoice.set(self.adb_choices[0])


        r = r + 25
        self.varAppTitle = StringVar()
        self.varAddressTitle = StringVar()
        self.varTimeTitle = StringVar()
        self.varAskTitle = StringVar()
        Label(self.master, textvariable=self.varAppTitle, font='Symbol 12 bold', relief=RIDGE).grid(row=r,column=0)
        Label(self.master, textvariable=self.varAddressTitle, font='Symbol 12 bold', relief=RIDGE).grid(row=r,column=1)
        Label(self.master, textvariable=self.varTimeTitle, font='Symbol 12 bold', relief=RIDGE).grid(row=r,column=2)
        Label(self.master, textvariable=self.varAskTitle, font='Symbol 12 bold', relief=RIDGE).grid(row=r,column=3)
        self.varAppTitle.set("App Name")
        self.varAddressTitle.set("Adress/IP")
        self.varTimeTitle.set("Time in min")
        self.varAskTitle.set("En/Dis")

        r = r + 20

        for widgetIdx, myWidget in enumerate(self.myWidgets):
            myWidget['name'] = self.widgets[widgetIdx]
            myWidget['label'] = StringVar()
            myWidget['addressText'] = StringVar()
            myWidget['time'] = IntVar()
            myWidget['chkbtn'] = IntVar()

            #.config(state = DISABLED)
            Label(self.master, textvariable=myWidget['label'], state=self.widget_status[widgetIdx], relief=SUNKEN).grid(row=r,column=0,padx=5, pady=5)
            myWidget['label'].set(myWidget['name'])
            if myWidget['name'] is 'Website':
                # Dictionary with options
                self.widget_text[widgetIdx]='wikilinks'
                choices = { 'wikilinks','http://www.time.com','http://www.nfl.com','http://www.cnn.com'}
                OptionMenu(self.master, myWidget['addressText'], *choices).grid(row=r, column=1, padx=5, pady=5)
            else:
                Entry(self.master, textvariable=myWidget['addressText'], state=self.widget_status[widgetIdx]).grid(row=r, column=1, padx=5, pady=5)
            myWidget['addressText'].set(self.widget_text[widgetIdx])

            Entry(self.master, textvariable=myWidget['time'], state=self.widget_status[widgetIdx]).grid(row=r, column=2, padx=5, pady=5)
            myWidget['time'].set(self.widget_time[widgetIdx])
            Checkbutton(self.master, text="", variable=myWidget['chkbtn'], state=self.widget_status[widgetIdx]).grid(row=r, column=3, padx=5, pady=5)
            myWidget['chkbtn'].set(self.widget_chkbox[widgetIdx])
            r = r + 1
            r = r + 10
            self.btnSubmit = Button(self.master, text="Go For It!", command=self.submit)
            self.btnSubmit.grid(row=r, column=1)
            self.btnClose = Button(self.master, text="Close", justify=RIGHT,command=self.close_button)
            self.btnClose.grid(row=r, column=2)
            self.btnClose = Button(self.master, text="Stop", justify=RIGHT,command=self.stop_all_process)
            self.btnClose.grid(row=r, column=3)


    def close_button(self):
        print("Inside Close button")
        self.queue.put("Stop")
        print("Queue putting Stop from Close button. Exiting now")
        time.sleep(1)
        self.master.quit()

    def stop_all_process(self):
    	self.queue.put("Stop")

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            print("Process_queue msg" +msg)
            # Show result of the task if needed
            if msg in "Stop":
                print(msg)
                self.master.destroy()
        except Empty:
            #print("The queue is empty -- printed from process_queue")
            self.master.after(100, self.process_queue)

    def submit(self):
    	#checkbutton variable type is integer (not str or bool)
        if self.myWidgets[0]['chkbtn'].get() and self.myWidgets[0]['time'].get()>0:
            print("Running website " + self.myWidgets[0]['addressText'].get() +" for "+str(self.myWidgets[0]['time'].get()))
            self.queue = Queue()
            self.activity = "browsing"
            ThreadedTask(self.queue, self.activity, self.myWidgets[0]['addressText'].get(), self.myWidgets[0]['time'].get()).start()
            self.master.after(100, self.process_queue)

        if self.myWidgets[1]['chkbtn'].get():
            pass
                #Run Youtube here
        if self.myWidgets[2]['chkbtn'].get():
            pass
                #Run Ping here

    #These prints are helpful to further our understanding
    #print("myWidgets[0]['name'] = " + str(myWidgets[0]['name']))
    #print("myWidgets[0]['label'] = " + myWidgets[0]['label'].get())
    #print("myWidgets[0]['time'] = " + str(myWidgets[0]['time'].get()))


class ThreadedTask(threading.Thread):
    def __init__(self, queue, activity, address, time):
        threading.Thread.__init__(self)
        self.queue = queue
        self.activity = activity
        self.address = address
        self.time = time
        self.sleep_duration = 1
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
                        start_webpage_command = "adb shell am start -a android.intent.action.VIEW -d " + webpage
                        os.system(start_webpage_command)
                        #print("Browsing " + webpage)
                        time.sleep(self.sleep_duration)
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
                else:
                    run_webpages(self.address)
                    time.sleep(self.sleep_duration)
