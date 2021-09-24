import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

p = GPIO.PWM(2, 50) 
p.start(0)
try:
    p.start(0)
    while True:
        dc = int(input("Введите напряжение в процентах от максимального > "))
        if dc>=0 and dc<=100:
            p.ChangeDutyCycle(dc)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()