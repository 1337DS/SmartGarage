#!/usr/bin/env python3
import cv2
import depthai as dai

#imports
from datetime import datetime
import re
kz = "KALF3006"

import cv2
import numpy as np
import imutils
import easyocr  

def openGarage(kennzeichen, lf, wl):
    #belegt status
    occupied = 0 #Ausblick
    #files
    log_file = open(lf, "a")

    #read logfile
    with open(lf) as file:
        lines = file.readlines()
        logs = [line.rstrip() for line in lines]

    #read whitelist
    with open(wl) as file:
        lines = file.readlines()
        whitelist = [line.rstrip() for line in lines]
    
    if len(logs) > 0:
        log = open("log.txt", "r")
        lines = log.readlines()
        last_line = lines[-1]
        ts = datetime.strptime(re.findall(".+?(?= ->)", last_line)[0], '%d/%m/%y %H:%M:%S')
    #if kennzeichen in whitelist dann Ã¶ffne
    if kennzeichen in whitelist and (len(logs) == 0 or int((datetime.now()-ts).seconds)>30) and occupied == 0:
        ts = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print(f"Garagentor wird geÃ¶ffnet fÃ¼r {kz}")
        log_file.write(f"{ts} -> {kz}\n")
    elif kz in whitelist and int((datetime.now()-ts).seconds)<=30:
        print(f"In {30-int((datetime.now()-ts).seconds)} Sekunden wieder verfÃ¼gbar")
    else:
        print("Kennzeichen nicht in Whitelist")

def openGarageAlexa(lf):
    #files
    log_file = open(lf, "a")

    #read logfile
    with open(lf) as file:
        lines = file.readlines()
        logs = [line.rstrip() for line in lines]
    
    if len(logs) > 0:
        log = open("log.txt", "r")
        lines = log.readlines()
        last_line = lines[-1]
        ts = datetime.strptime(re.findall(".+?(?= ->)", last_line)[0], '%d/%m/%y %H:%M:%S')
    #if kennzeichen in whitelist dann Ã¶ffne
        ts = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print(f"Garagentor wird geÃ¶ffnet fÃ¼r Alexa")
        log_file.write(f"{ts} -> Alexa\n")

# Start defining a pipeline
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
    img = device.getOutputQueue("still").get()
    cv2.imwrite('still.jpg', img.getCvFrame())
    
    img = cv2.imread('still.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 100) #Edge detection
    #plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    print(location)
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    
    #plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    print(result)
    
    text = str.upper(result[0][1])
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
    
    plt.imwrite('test2.jpg',cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
