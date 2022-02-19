import cv2
import numpy as np
import imutils
from os import listdir
from os.path import isfile, join
import pytesseract
from PIL import Image
import depthai as dai
# Wichtig!
#pip install opencv-python==4.5.4.6
###KAMERA

while True:	# Start defining a pipeline
	pipeline = dai.Pipeline()

	# Define a source - color camera
	cam = pipeline.create(dai.node.ColorCamera)

	# Script node
	script = pipeline.create(dai.node.Script)
	script.setScript("""
	    import time
	    ctrl = CameraControl()
	    ctrl.setCaptureStill(True)
	    while True:
	        time.sleep(1)
	        node.io['out'].send(ctrl)
	""")

	# XLinkOut
	xout = pipeline.create(dai.node.XLinkOut)
	xout.setStreamName('still')

	# Connections
	script.outputs['out'].link(cam.inputControl)
	cam.still.link(xout.input)

	# Connect to device with pipeline
	#while true:

	with dai.Device(pipeline) as device:
	    
	        # funktioniert leider nicht
	    #controlQueue = device.getInputQueue('control')
	    #ctrl = dai.CameraControl()
	    #ctrl.setCaptureStill(True)
	    #controlQueue.send(ctrl)
	    #img = device.getOutputQueue("still").get()
	    #cv2.imwrite('still2.jpg', img.getCvFrame())

	    img = device.getOutputQueue("still").get()
	    cv2.imwrite('still.jpg', img.getCvFrame())






	###OCR TEil

	img = cv2.imread(r"still.jpg")

	#pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
	edged = cv2.Canny(bfilter, 30, 100) #Edge detection
	#plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
	#plt.show()
	keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(keypoints)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
	location = None
	for contour in contours:
	    approx = cv2.approxPolyDP(contour, 10, True)
	    if len(approx) == 4:
	        location = approx
	        break

	    #print(location)

	mask = np.zeros(gray.shape, np.uint8)
	new_image = cv2.drawContours(mask, [location], 0,255, -1)
	new_image = cv2.bitwise_and(img, img, mask=mask)


	(x,y) = np.where(mask==255)
	(x1, y1) = (np.min(x), np.min(y))
	(x2, y2) = (np.max(x), np.max(y))
	cropped_image = gray[x1:x2+1, y1:y2+1]
	cv2.imwrite('cropped.jpg',cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

	txt = pytesseract.image_to_string(cropped_image, config="--psm 6")  
	print(f"Vor ganzem Zeug:{txt}")
	txt = txt.replace(";", "")
	txt = txt.replace(":", "")
	txt = txt.replace(",", "")
	txt = txt.replace(".", "")
	txt = txt.replace(" ","")
	txt = txt.replace("°","").lower()
	txt = txt.lower()
	txt = txt.strip()
	texts = [txt,txt.replace("o","0"),txt.replace("0","o")]
	print(texts)



