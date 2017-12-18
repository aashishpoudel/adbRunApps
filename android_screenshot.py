import datetime
import subprocess

#The below works in python command prompt
#>>> subprocess.Popen(["adb","push","temp1.txt","/dev"],stdout=subprocess.PIPE, shell=True).communicate()[0]

def wincommand_output(mycmd, myarg):
	#print("subprocess.Popen called")
	p = subprocess.Popen([mycmd, myarg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	return p.communicate()[0]

def print_timestamp():
	return datetime.datetime.now().strftime('%Y-%m-%d.%H%M%S')

def devicetimestamp():
	datestatus = wincommand_output("adb shell date +%Y%m%d_%H%M%S","")
	if(datestatus):
		print(datestatus)
	return datestatus

def deviceserial():
	deviceSNFull = wincommand_output("adb devices","-l")
	print("deviceSNFull = " +deviceSNFull)
	return deviceSNFull

def adbscreencapture():
	#filename = "screenshot" + "_" + deviceserial() + "_" + devicetimestamp() + ".png"
	filename = "screenshot" + "_" + print_timestamp() + ".png"
	#filename = "screenshot.png"
	print(print_timestamp() + " " + "---saving " + filename)
	screencap_command = "adb shell screencap -p /data/local/" + filename
	screencap_command_list = screencap_command.split()
	print("screencap_command_list = " + str(screencap_command_list))
	p=subprocess.Popen(screencap_command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	print("Screencap Command Status = " + p.communicate()[0])
	#print(wincommand_output("adb","devices"))
	#Pulling to computer
	pullcommand = "adb pull /data/local/"+filename
	pullcommand_list = pullcommand.split()
	print("pullcommand_list = " + str(pullcommand_list))
	p=subprocess.Popen(args=pullcommand_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	#Deleting from the Android phone


#Main Part of Program
print(str(datetime.datetime.now()) + "--Waiting for device")
subprocess.Popen(["adb wait-for-device root",""], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
subprocess.Popen(["adb wait-for-device",""], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

#print(timestamp())
#print(deviceserial())
print(devicetimestamp())
adbscreencapture()
