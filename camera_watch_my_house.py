#!/usr/bin/env python
import cv2
import time
import datetime
import ConfigParser
import sys

config=ConfigParser.RawConfigParser()
config.read('config.cfg')
saveLocation=config.get('FileLocation','saveDir')
fileName=config.get('FileLocation','fileName')
fileCounter=int(config.get('FileLocation','fileCount'))

imageText=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
dataFileText=datetime.datetime.now().strftime('%Y-%m-%d/t%H:%M:%S')

camera_index = 0; x=0; y=50
capture = cv2.VideoCapture(camera_index)
ret, photo=capture.read()

if ret:
	print "Camera successful"
	print imageText

	print saveLocation

	cv2.putText(photo,imageText, (x,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),1)

	capture.release()

	retVal=cv2.imwrite(saveLocation + fileName + str(fileCounter)+ ".jpg",photo)
	if retVal:
		print "Saved"
		print "Filecounter: %i" %fileCounter
		fileCounter+=1
		config.set('FileLocation','fileCount',str(fileCounter))
		
		with open('config.cfg', 'w') as configfile:    # save
			config.write(configfile)
	else:
		print "Save Failed"

	cv2.imshow("Camera_Test",photo)
	cv2.waitKey(5000)
	cv2.destroyAllWindows()
else :
		print "Camera Error"
