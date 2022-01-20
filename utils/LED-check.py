import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)

GPIO.setup(20, GPIO.IN)

#GPIO.input(21)

while True:
        if GPIO.input(20)== 0:
	        pass
        else:
        	print("Alexa-Befehl empfangen")
		GPIO.output(21, GPIO.HIGH)

