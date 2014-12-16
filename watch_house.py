#!/usr/bin/env python
import cv2
import time
import datetime
import serial


def main():
		
	fileLocation ="/home/jamie/Dropbox/"
	d=datetime.datetime.now().strftime('%Y-%m-%d\t%H:%M:%S')
	
	#Get temperature data from Arduino
	arduinoTemp=getData(d,fileLocation)
	print "Temperature %0.1f" %(arduinoTemp)
	
	if arduinoTemp !='NULL':
		returnSave=saveData(d,arduinoTemp,fileLocation)
	else:
		print "No data"
	
	#Get Image from Camera
	retImage=getImage(d,arduinoTemp, returnSave['nr_of_lines'],fileLocation)
	if retImage:
		print "Saved image successfully at %s" % d
	else:
		print "Saved image failed at %s" % d
	return 0
	


def getImage(d,temperature,nr_of_lines,fileLocation):
	
	camera_index = 0; x=0; y=50
	capture = cv2.VideoCapture(camera_index)
	ret, photo=capture.read()
	if ret:	
		print "Camera successful"
		
		#Put temperature data on image
		cv2.putText(photo,"Temp: %0.1f" % (temperature), (x,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
		cv2.putText(photo,d, (x,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)

		#Save image
		try:
			retVal=cv2.imwrite(fileLocation+"Kitchen_"+str(nr_of_lines)+".jpg",photo)
		except IOError as e:
			print "Image save error" + e
			success=0
		else:
			success =1
		capture.release()
		
		#cv2.imshow("Kitchen_Camera",photo)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()	
	else:
		print "camera error"
		success = 0
	return success


def getData(d,fileLocation):
	port="/dev/ttyUSB0"
	baudrate=9600
	
	try:
		arduinoSerial=serial.Serial(port,baudrate)
		time.sleep(2) # waiting the initialization...
		
		arduinoSerial.write('r')
		time.sleep(2) # waiting the initialization...
		data=arduinoSerial.readline()
		data=data.rstrip('\r\n')
		arduinoSerial.close()
		data=500*float(data)/1024
		
	except:
		print "Can not open Arduino on port:", port," at time:",datetime.datetime.now()
		data="NULL"
	return data

def saveData(dateTime,data, fileLocation):
	try:
		f=open(fileLocation+"tempdata.csv","r")
		nr_of_lines = sum(1 for line in f)-1
		f.close()
	except IOError:
		f=open(fileLocation+"tempdata.csv","w")
		makeFileHeaders="Row\t"+"Date\t"+"Time\t"+"Temp (C)\n"
		f.write(makeFileHeaders)
		f.close
		nr_of_lines=0
		
	with open(fileLocation+"tempdata.csv","a") as f:
		mydata= str(nr_of_lines)+"\t"+dateTime +"\t"+ str(data)+"\n"
		f.write(mydata)

	return {'nr_of_lines':nr_of_lines}

if __name__ == '__main__':
	main()

