# -*- coding: utf-8 -*-
'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: https://randomnerdtutorials.com

Modified by Andreas Edte for Project SmartGarage
'''


import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time
import os
from datetime import datetime
import re
app = Flask(__name__)

# Setzen der GPIO Ein-/Ausgaenge
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21, GPIO.OUT)

GPIO.setup(20, GPIO.IN)

lf = "/home/pi/garage/logs.txt"

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   # Put the pin dictionary into the template data dictionary:
   templateData = {'test'}
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html')

# Diese Funktion wird bei Klick auf den Open Button ausgefuhrt:
@app.route("/activate")
def action():
    GPIO.output(21, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(21, GPIO.LOW)
    
    
# Eintrag ins Logfile
    log_file = open(lf, "a")

    #read logfile
    with open(lf) as file:
        lines = file.readlines()
        logs = [line.rstrip() for line in lines]
    
    if len(logs) > 0:
        log = open(lf, "r")
        lines = log.readlines()
        last_line = lines[-1]
        ts="01.01.2022"
        # @ Luca debugging necessary here        
        #ts = datetime.strptime(re.findall(".+?(?= ->)", last_line)[0], '%d/%m/%y %H:%M:%S')
    #if kennzeichen in whitelist dann öffne
        ts = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print("Garage-door opened for Web-App")
        log_file.write("{ts}; Website\n") 
    
    
    
    
    return render_template('main.html')

@app.route('/logs')
def info():
      with open(lf) as f:
        logdata = f.readlines()
        return render_template('logs.html',logdata=logdata)
      
      
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)