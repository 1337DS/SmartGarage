#!/usr/bin/env python3
import cv2
import depthai as dai

#imports
from datetime import datetime
import re
kz = "KALF3006"

import numpy as np
import imutils

import pytesseract
from difflib import SequenceMatcher
#import easyocr  

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
    
        # funktioniert leider nicht
    #controlQueue = device.getInputQueue('control')
    #ctrl = dai.CameraControl()
    #ctrl.setCaptureStill(True)
    #controlQueue.send(ctrl)
    #img = device.getOutputQueue("still").get()
    #cv2.imwrite('still2.jpg', img.getCvFrame())

    img = device.getOutputQueue("still").get()
    cv2.imwrite('still2.jpg', img.getCvFrame())
    
    img = cv2.imread('still2.jpg')
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
    
    cv2.imwrite('cropped.jpg',cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    
    
###########################################################
#reader = easyocr.Reader(['en'])
#result = reader.readtext(cropped_image)



#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

image = cropped_image #cv2.imread("C:/Users/lucaf/Desktop/cropped99.jpg") 

txt = pytesseract.image_to_string(image, config="--psm 6")  
print(f"alt: {txt}")
txt = txt.replace(";", "")
txt = txt.replace(":", "")
txt = txt.replace(",", "")
txt = txt.replace(".", "")
txt = txt[:-5].replace("0","O")+txt[-5:]
print(f"neu: {txt}")
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


#print(similar("OG AE 1337".lower().strip(" "), txt.lower().strip(" ")))
print('Ergebnis:',txt)





















#print(result)
dic_ocr={}

#for x in result:

#    pointA=x[0][0]
#    pointC=x[0][2]
#    AC=[pointC[0]-pointA[0],pointC[1]-pointA[1]]
#    up2=np.power(AC,2)
#    up2=sum(up2)
#    diagon=np.sqrt(up2)
    # print(x[1])
    # print(diagon)
#    dic_ocr[diagon]=[int(x[0][0][0]),x[1]]




#value_max=max(dic_ocr.items())[0]



#biggest_box_last_layer=(max(dic_ocr.items())[0])/1.5


#dic_ocr2=dic_ocr.copy()



#for i in dic_ocr2:
#    if i<biggest_box_last_layer:
#        dic_ocr.pop(i)



#x=list(dic_ocr.values())
#sorted_list=sorted(x, key=lambda x: x[0], reverse=False) # Von links nach rechts lesen

#checkplate=("".join([new[1] for new in sorted_list]))
#print(checkplate)

white_list=["EBEOK106","HDPM2819"] #nacher rauskommentieren
def check_plates(check,white_list):

    for x in white_list:
        if check==x:
            print("open die scheiss door")
    # permutations = list(itertools.permutations(check))
    # kz_list = [''.join(part) for part in permutations]

    # print(kz_list)
    # for check_plate in kz_list:
    #     if check_plate in white_list:
    #         print("open")
check_plates(txt, white_list)
#check_plates(checkplate,white_list)

    
