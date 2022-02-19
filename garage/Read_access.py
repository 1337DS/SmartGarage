#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from utils.buzzer_confirm_deny import deny, confirm
reader = SimpleMFRC522()
wl = "whitelist_rfid.txt"
from utils.sim_auf import start as sim_auf
from utils.sim_zu import start as sim_zu
status_path = "./status.txt"

with open(wl) as file:
        lines = file.readlines()
        whitelist = [line.rstrip() for line in lines]
        whitelist=["1337"]

while True:
  try:
    print("anfang")
    id, text = reader.read()  
    print(id)
    print(text)
    print(type(text))
    text=str(text)
    print(type(text))
    print(whitelist)
    for line in whitelist:
      print('Eintrag:',line)
      print(type(line))
      if line in text:
        print("Access granted")
        confirm()
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
            print("test1")
        elif int(status) == 1:
          with open(status_path, "w") as sfile:
            sfile.write("0")
            print("write0")
            sim_zu()
            print("test2")
      else:
        print("Access denied")
        deny
  except KeyboardInterrupt:
    print('interrupted!')
    break
  




