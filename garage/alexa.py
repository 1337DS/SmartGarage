# Endlosschleife
import RPi.GPIO as GPIO

from utils.sim_auf import start as sim_auf
from utils.sim_zu import start as sim_zu
status_path = "./status.txt"
GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.IN)
while True:
    if GPIO.input(22) == 1:
        print("gleich passiert was")
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
    else:
        # Einschalten
        pass
    