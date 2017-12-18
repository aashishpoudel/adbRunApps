import datetime
import subprocess
import os
import time

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

sleep_duration = 15
total_duration_in_min = 30

def adb_sites(webpage):
	print(print_timestamp() + " " + "---Browsing " + webpage)
	start_webpage_command = "adb shell am start -a android.intent.action.VIEW -d " + webpage
	start_webpage_command_list = start_webpage_command.split()
	os.system(start_webpage_command) #For ubuntu. NOt sure why subprocess not working
	#print("start_webpage_command_list = " + str(start_webpage_command_list))
    #p=subprocess.Popen(start_webpage_command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #print("start_webpage Command Status = " + p.communicate()[0])


#Main Part of Program
timestart = datetime.datetime.now()
print(str(timestart) + "--Waiting for device")
subprocess.Popen(["adb wait-for-device root",""], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

time.sleep(5)
#lapsed_duration = (datetime.datetime.now()-timestart).minute
timesince = datetime.datetime.now() - timestart
minutessince = int(timesince.total_seconds() / 60)

while minutessince < total_duration_in_min:
    for webpage in websites_lists:
        #print(webpage)
        adb_sites(webpage)
        time.sleep(sleep_duration)
    timesince = datetime.datetime.now() - timestart
    minutessince = int(timesince.total_seconds() / 60)
    print("Elapsed min = "+str(minutessince))
