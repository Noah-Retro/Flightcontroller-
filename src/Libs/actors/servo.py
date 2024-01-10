import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(03, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(03, False)
    p.ChangeDutyCycle(0)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 als PWM mit 50Hz
p.start(4) # Initialisierung
try:
  while True:
    setAngle(0)
    setAngle(90)
    setAngle(180)
    
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()