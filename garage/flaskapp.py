'''
Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: https://randomnerdtutorials.com

Modified by Andreas Edte for Project SmartGarage
Anleitung: 
-Pfad der Log Datei anpassen.
-GPIO kommentierung aufheben


'''
from utils.sim_auf import start as sim_auf
from utils.sim_zu import start as sim_zu
import sys
#import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time
import os
from datetime import datetime
import re
import pywhatkit
import keyboard as k
import ultraschallsensor


app = Flask(__name__)

# Setzen der GPIO Ein-/Ausgaenge
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#GPIO.setup(21, GPIO.OUT)

#GPIO.setup(20, GPIO.IN)

#lf = "/home/pi/garage/logs.txt"
lf_path = r"./logs.txt"
#lf = open(lf_path, encoding="UTF-8", mode="w")
status_path =r"./status.txt"

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   # Put the pin dictionary into the template data dictionary:
   templateData = {'test'}
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', distanz=ultraschallsensor.distanz())

# Diese Funktion wird bei Klick auf den Open Button ausgefuhrt:
@app.route("/activate")
def action():
    #GPIO.output(21, GPIO.HIGH)
    #time.sleep(1)
    #GPIO.output(21, GPIO.LOW)
    print(1)
    with open(status_path, "r") as sfile:
        status = sfile.read()
        sfile.close()
    print(2)
    print(f"status={status}")
    if int(status) == 0:
        with open(status_path, "w") as f:
            f.write("1")
            print("write1")
        sim_auf()
    elif int(status) == 1:
        with open(status_path, "w") as sfile:
            sfile.write("0")
            print("write0")
        sim_zu()
    now = datetime.now()
    time = now.strftime("%d Jan %H:%M:%S")
    #pywhatkit.sendwhatmsg_instantly("+49 178 8899478", f'Garage geöffnet durch Weboberfläche {time}',25, True, 5)
    #pywhatkit.sendwhatmsg_to_group_instantly("L2wDsVunQhe4Zl5DkOTv90",  f'Garage geöffnet durch Weboberfläche {time}', 15, True, 5)
    with open(lf_path, "a") as file:	
        file.writelines(f"{time} -> WebApp\n")
        file.close()

# Eintrag ins Logfile
        #log_file = open(lf, "a")

    #read logfile
  
        # @ Luca debugging necessary here        
        #ts = datetime.strptime(re.findall(".+?(?= ->)", last_line)[0], '%d/%m/%y %H:%M:%S')
    #if kennzeichen in whitelist dann �ffne
        # ts = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        # print("Garage-door opened for Web-App")
        # log_file.write("{ts}; Website\n") 
    
    
    
    
    return render_template('main.html', distanz=ultraschallsensor.distanz())

@app.route('/logs')
def info():
    with open(lf_path) as file:
        logdata = file.readlines()
    return render_template('logs.html',logdata=logdata, distanz=ultraschallsensor.distanz())
      
      
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
