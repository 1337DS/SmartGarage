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
app = Flask(__name__)

# Setzen der GPIO Ein-/Ausgaenge
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21, GPIO.OUT)

GPIO.setup(20, GPIO.IN)



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
    return render_template('main.html')

@app.route('/logs')
def info():
      with open("/home/pi/garage/logs.txt") as f:
        logdata = f.readlines()
        return render_template('logs.html',logdata=logdata)
        
      
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)