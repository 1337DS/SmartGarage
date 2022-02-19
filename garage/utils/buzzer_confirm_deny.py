
#Libraries
import RPi.GPIO as GPIO
from time import sleep
#Disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)
#Set buzzer - pin 23 as output
buzzer=4 
GPIO.setup(buzzer,GPIO.OUT)
#Run forever loop
#from LED import LED


def deny():
  for x in range(3):
      GPIO.output(buzzer,GPIO.HIGH)
      print ("Beep")
      sleep(0.35) # Delay in seconds
      GPIO.output(buzzer,GPIO.LOW)
      print ("No Beep")
      #LED()
      sleep(0.2)
      
def confirm():
    for x in range(1):
      GPIO.output(buzzer,GPIO.HIGH)
      sleep(0.9)
      GPIO.output(buzzer,GPIO.LOW)
      print ("No Beep")
      #LED()
      sleep(0.9)

      
      
      
      
      
