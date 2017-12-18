import datetime
import subprocess
import time
import os
import collections
from tkinter import *

def print_timestamp():
	return datetime.datetime.now().strftime('%Y-%m-%d.%H%M%S')

youtube_sites =["https://www.youtube.com/watch?v=Lamg_hJVW_U", # 0:32
                "https://www.youtube.com/watch?v=VESKjoxAmZg", # 0:33
                "https://www.youtube.com/watch?v=YVyWObJY9FQ", # 0:55
                "https://www.youtube.com/watch?v=iWC-2nKAgic", # 1:16
                "https://www.youtube.com/watch?v=bbThSb2DImk", # 1:41
                "https://www.youtube.com/watch?v=NDyYvpqp46w", # 2:21
                ]

websites_lists =["https://www.youtube.com/watch?v=Lamg_hJVW_U", # 0:32
                "https://www.youtube.com/watch?v=VESKjoxAmZg", # 0:33
                "https://www.youtube.com/watch?v=YVyWObJY9FQ", # 0:55
                "https://www.youtube.com/watch?v=iWC-2nKAgic", # 1:16
                "https://www.youtube.com/watch?v=bbThSb2DImk", # 1:41
                "https://www.youtube.com/watch?v=NDyYvpqp46w", # 2:21
                ]

#https://en.m.wikipedia.org/wiki/1945
websites_lists =["https://en.m.wikipedia.org/wiki/" + str(i) for i in range (1850,2017)]

sleep_duration = 2
total_duration_in_min = 30



window=Tk()

r=0
varADB = StringVar()
varADBentry = StringVar()
Label(window, textvariable=varADB, font='Helvetica 15 bold', relief=SUNKEN).grid(row=r,column=0)
varADB.set("ADB Devices")
Entry(window, textvariable=varADBentry).grid(row=r, column=1, rowspan=25)
varADBentry.set("No Devices")

r = r + 25
varAppTitle = StringVar()
varAddressTitle = StringVar()
varTimeTitle = StringVar()
varAskTitle = StringVar()
Label(window, textvariable=varAppTitle, font='Symbol 12 bold', relief=RIDGE).grid(row=r,column=0)
Label(window, textvariable=varAddressTitle, font='Symbol 12 bold', relief=RIDGE).grid(row=r,column=1)
Label(window, textvariable=varTimeTitle, font='Symbol 12 bold', relief=RIDGE).grid(row=r,column=2)
Label(window, textvariable=varAskTitle, font='Symbol 12 bold', relief=RIDGE).grid(row=r,column=3)
varAppTitle.set("App Name")
varAddressTitle.set("Adress/IP")
varTimeTitle.set("Time in min")
varAskTitle.set("En/Dis")

def adb_sites(webpage):
	print(print_timestamp() + " " + "---Browsing " + webpage)
	start_webpage_command = "adb shell am start -a android.intent.action.VIEW -d " + webpage
	#start_webpage_command = "adb shell am start -W -a android.intent.action.VIEW -d \"http://example.com/gizmos\""
	start_webpage_command = "adb shell am start -W -a android.intent.action.VIEW -d " + webpage
	start_webpage_command_list = start_webpage_command.split()
	print(start_webpage_command)
	os.system(start_webpage_command)
	#print("start_webpage_command_list = " + str(start_webpage_command_list))
    #p=subprocess.Popen(start_webpage_command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #print("start_webpage Command Status = " + p.communicate()[0])

def goforit():
	#checkbutton variable type is integer (not str or bool)
	if myWidgets[0]['chkbtn'].get():
		#print("check2")
		#print(myWidgets[0]['addressText'].get())
		print("You provided website as " + myWidgets[0]['addressText'].get() +". Good luck!")
		if(myWidgets[0]['time'].get()>0):
			#Main Part of Program
			timestart = datetime.datetime.now()
			print(str(timestart) + "--Waiting for device")
			os.system("adb wait-for-device devices")
			#subprocess.Popen(["adb wait-for-device devices",""], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			time.sleep(5)
			#lapsed_duration = (datetime.datetime.now()-timestart).seconds
			timesince = datetime.datetime.now() - timestart
			minutessince = int(timesince.total_seconds() / 60)
			secondsince = int(timesince.total_seconds())

			while minutessince < int(myWidgets[0]['time'].get()):
				#Common mistake point. Compare string with 'in'
				if str(myWidgets[0]['addressText'].get()) in 'wikilinks':
					for webpage in websites_lists:
						start_webpage_command = "adb shell am start -a android.intent.action.VIEW -d " + webpage
						os.system(start_webpage_command)
						#time.sleep(sleep_duration)
				else:
					adb_sites(myWidgets[0]['addressText'].get())
					time.sleep(sleep_duration)
				timesince = datetime.datetime.now() - timestart
				minutessince = int(timesince.total_seconds() / 60)
				secondsince = int(timesince.total_seconds())
				print("Elapsed min = "+str(minutessince))
				print("Elapsed sec = "+str(secondsince))
		else:
			print("Please enter a valid time for " + myWidgets[0]['label'].get())
		#Run website here
		#t1.insert(END,mile)
	if myWidgets[1]['chkbtn'].get():
		pass
		#Run Youtube here
	if myWidgets[2]['chkbtn'].get():
		pass
		#Run Ping here

r = r + 20
widgetIdx = 0

#This creates multiple myWidgets dictionaries
widgets = ['Website','Youtube','Ping']
myWidgets = [dict() for i in range(len(widgets))]
widgets_label = ['Website','Youtube','Ping']
widget_text =['','','']
widget_time = [30,40,50]
widget_chkbox = [1,0,0]

for myWidget in myWidgets:
	myWidget['name'] = widgets[widgetIdx]
	myWidget['label'] = StringVar()
	myWidget['addressText'] = StringVar()
	myWidget['time'] = IntVar()
	myWidget['chkbtn'] = IntVar()

	Label(window, textvariable=myWidget['label'], relief=SUNKEN).grid(row=r,column=0,padx=5, pady=5)
	myWidget['label'].set(myWidget['name'])
	if myWidget['name'] is 'Website':
		# Dictionary with options
		widget_text[widgetIdx]='wikilinks'
		choices = { 'wikilinks','http://www.time.com','http://www.nfl.com','http://www.cnn.com'}
		OptionMenu(window, myWidget['addressText'], *choices).grid(row=r, column=1, padx=5, pady=5)
	else:
		Entry(window, textvariable=myWidget['addressText']).grid(row=r, column=1, padx=5, pady=5)
	myWidget['addressText'].set(widget_text[widgetIdx])

	# on change dropdown value
	#def change_dropdown(*args):
	#    print( tkvar.get() )
	#print(myWidgets[0]['addressText'].get())
	#print(str(myWidgets[0]['addressText'].get()))
	Entry(window, textvariable=myWidget['time']).grid(row=r, column=2, padx=5, pady=5)
	myWidget['time'].set(widget_time[widgetIdx])
	Checkbutton(window, text="", variable=myWidget['chkbtn']).grid(row=r, column=3, padx=5, pady=5)
	myWidget['chkbtn'].set(widget_chkbox[widgetIdx])
	r = r + 1
	widgetIdx = widgetIdx+1

#These prints are helpful to further our understanding
#print("myWidgets[0]['name'] = " + str(myWidgets[0]['name']))
print("myWidgets[0]['label'] = " + myWidgets[0]['label'].get())
print("myWidgets[0]['time'] = " + str(myWidgets[0]['time'].get()))

r = r + 10
btnSubmit = Button(window, text="Go For It!", command=goforit)
btnSubmit.grid(row=r, column=1)

# If no window.mainloop() below, GUI ll be quickly gone in blink of an eye
window.mainloop()
