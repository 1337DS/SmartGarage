import RPi.GPIO as GPIO
from time import sleep


def LED():
  GPIO.setmode(GPIO.BCM)
  
  GPIO.setup(26, GPIO.OUT)
  
  GPIO.output(26, GPIO.HIGH)
  sleep(5)
  GPIO.output(26, GPIO.LOW)

if __name__ == "__main__":
  LED()

