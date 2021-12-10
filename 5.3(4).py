import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt


leds = [21, 20, 16, 12, 7, 8, 25, 23]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comparator = 4
troykaVoltage = 17

bits = len(dac)
levels = 2 ** bits
dV = 3.3 / levels

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds + dac, GPIO.OUT)
GPIO.setup(troykaVoltage, GPIO.OUT)
GPIO.setup(comparator, GPIO.IN)


def pins(pins, value):
    GPIO.output(pins, [int(i) for i in bin(value)[2:].zfill(bits)])

def adc1():

    value = 0
    up = True

    for i in range(bits):
        delta = 2 ** (bits - 1 - i)
        value = value + delta * (1 if up else -1)

        pins(dac, value)
        time.sleep(0.0011)

        up = bool(GPIO.input(comparator))

    return value

def adc2():
    mass = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(8):
        
        mass[i] = 1
        GPIO.output(dac, mass)
        time.sleep(0.001)

        if GPIO.input(comparator) == 0:
            mass[i] = 0
        

    return mass[0]*2**7 + mass[1]*2**6 + mass[2]*2**5 + mass[3]*2**4 + mass[4]*2**3 + mass[5]*2**2 + mass[6]*2**1 + mass[7]*2**0

try:
    # 1. Создаем переменные

    measure = []
    value = 0
    measurePeriod = 0


    # 2. Фиксируем начальное время
    
    start = time.time()


    # 3. Зарядка конденсатора
    
    GPIO.output(troykaVoltage, 1)
    print('Зарядка конденсатора')
    while value <= 235:
        value = adc2()
        pins(leds, value)
        measure.append(value)
    

    # 4. Разрядка конденсатора

    GPIO.output(troykaVoltage, 0)
    print('Разрядка конденсатора')
    while value > 1:
        value = adc2()
        pins(leds, value)
        measure.append(value)

    # 5. Фиксируем время окончания и выводим значения времени

    finish = time.time()

    totalTime = finish - start
    measurePeriod = totalTime / len(measure) 
    Frequency = int(1 / measurePeriod)

    print("Общее время измерений: {:.2f} s, Период измерений: {:.3f} ms, Частота дискретизации: {:d} Hz".format(totalTime, measurePeriod, Frequency))
    print("Шаг напряжения: {:.3f} V".format(dV))

    # 6. График полученных измерений

    plt.plot(measure)
    plt.show()

    measure_str = [str(i) for i in measure]
    with open ("data.txt", "w") as outfile:
        outfile.write("\n".join(measure_str))
    massive = [time, measurePeriod, Frequency, dV]
    massive_str = [str(item) for item in massive]
    with open ("settings.txt", "w") as f:
        f.write("\n".join(massive_str))

finally:
    GPIO.cleanup()
    print('GPIO cleanup completed.')
\\
