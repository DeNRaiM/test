import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2**bits
maxU = 3.3
troyka = 17
comp = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac + leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)


def dec2bin (value):
    return [int(bin) for bin in bin(value)[2:].zfill(bits)]

def bin2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    value = 0
    for i in range(8):
        value = value + 2**(7 - i)
        signal = bin2dac(value)
        time.sleep(0.001)
        compValue = GPIO.input(comp)
        if compValue == 0:
            value = value - 2**(7 - i)
        voltage = value / levels * maxU
    print (" Digital value: {:^3} -> {}, Analog value: {:.2f}".format(value, signal, voltage))
    return voltage

def volumeBar():
    volume = adc()
    if (volume == 0):
        GPIO.output(leds, 0)
    for i in range(8):
        if (volume > maxU * i / bits):
            GPIO.output(leds[i], 1)          

try:
    while True:
        volumeBar() 
finally:
    GPIO.cleanup()