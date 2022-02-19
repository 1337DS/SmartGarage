#imports
from datetime import datetime
import re
kz = "KALF3006"

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
    #if kennzeichen in whitelist dann öffne
    if kennzeichen in whitelist and (len(logs) == 0 or int((datetime.now()-ts).seconds)>30) and occupied == 0:
        ts = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print(f"Garagentor wird geöffnet für {kz}")
        log_file.write(f"{ts} -> {kz}\n")
    elif kz in whitelist and int((datetime.now()-ts).seconds)<=30:
        print(f"In {30-int((datetime.now()-ts).seconds)} Sekunden wieder verfügbar")
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
    #if kennzeichen in whitelist dann öffne
        ts = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print(f"Garagentor wird geöffnet für Alexa")
        log_file.write(f"{ts} -> Alexa\n")


	
