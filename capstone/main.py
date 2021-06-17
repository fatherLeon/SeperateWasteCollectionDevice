import cv2
import time
import glob
import serial
import numpy as np
import tensorflow as tf

def findCamera():
	print("finding Camera")
	while True:
		time.sleep(10)
		cameraPort = glob.glob("/dev/video*")
		if len(cameraPort) > 0:
			print(cameraPort)
			return cameraPort[0]

def findPort():
	print("Find Port")
	while True:
		portList = glob.glob("/dev/ttyACM*")
		print(portList)
		if len(portList) > 2:
			return portList

def takePicture():
	cap = cv2.VideoCapture(0)
	_, img = cap.read()
	cap.release()
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = img / 255
	img = cv2.resize(img, dsize=(60, 60), interpolation=cv2.INTER_AREA)
	return img.reshape(1, 60, 60, 3)


print("Loading Model")
model = tf.keras.models.load_model("/home/kangminsu/Desktop/capstone/model/model.h5")
portList = findPort()
LINEAR_PORT = portList[-1]
SUBO_PORT = portList[-3]
DISTANCE_PORT = portList[-2]

linear = serial.Serial(LINEAR_PORT, 9600)
print("LINEAR Arduino")
time.sleep(2)
subo = serial.Serial(SUBO_PORT, 9600)
print("SUBO Arduino")
time.sleep(2)
distance = serial.Serial(DISTANCE_PORT, 9600)
print("DISTANCE Arduino")
time.sleep(2)

cameraPort = findCamera()
cap = cv2.VideoCapture(0)

boolean, _ = cap.read()
if boolean:
	print("Camera ON")
	cap.release()
else:
	print("Camera Error")
	cap.release()

while True:
	try:
		distanceValue = int(distance.readline().decode())
	except:
		distaneValue = 20
	print(distanceValue)
	if distanceValue < 10:
		time.sleep(1)
		img = takePicture()
		result = np.argmax(model.predict(img))
		if result == 0:
			print("non-trans")
			try:
				subo.write(str.encode("1"))
			except:
				portList = findPort()
				time.sleep(3)
				subo = serial.Serial(portList[0])
				time.sleep(3)
				subo.write(str.encode("1"))
			time.sleep(5)
			count = 0
			for x in range(6):
				try:
					distanceValue = int(distance.readline().decode())
				except:
					distaneValue = 20
				print(f"{count}delay{distanceValue}")
				count += 1
			#subo.close()
			#subo.open()
		else:
			print("trans")
			linear.write(str.encode("1"))
			time.sleep(50)
			try:
				subo.write(str.encode("0"))
			except:
				portList = findPort()
				time.sleep(3)
				subo = serial.Serial(portList[0])
				time.sleep(3)
				subo.write(str.encode("0"))
			count = 0
			for x in range(13):
				try:
					distanceValue = int(distance.readline().decode())
				except:
					distaneValue = 20
				print(f"{count}delay{distanceValue}")
				count += 1
			#subo.close()
			#linear.open()
			#subo.open()
