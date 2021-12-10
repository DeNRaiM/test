import numpy as np
import matplotlib.pyplot as plt

with open("settings.txt", "r") as settings:
    tmp = [float(i) for i in settings.read().split("\n")]

data_array = np.loadtxt("data.txt", dtype=int)
time_array = []
voltage_array = data_array*tmp[0]
for i in range(len(voltage_array)):
    time_array.append(i*tmp[1])   
max_voltage = max(voltage_array)
min_voltage = min(voltage_array)

i=1
while voltage_array[i] != max_voltage:
    i+=1
else: 
    max_time=i
print(max_time)

i=1
while voltage_array[i] != min_voltage:
    i+=1
else: 
    min_time=i
print(min_time)

time=min_time-max_time
print(time)

fig, ax = plt.subplots(figsize=(16, 10), dpi = 150)

ax.plot(time_array, voltage_array, "b", linewidth = '1.0', marker = '+', markevery = 50, markersize = '15.0')
ax.minorticks_on()
ax.set_title("График зависимости напряжения от времени")
ax.set_xlabel('время, (с)')
ax.set_ylabel('напряжение, (В)')
ax.grid(which="major", linewidth=0.5, color='red')
ax.grid(which="minor", linestyle="--", color='k', linewidth=0.3)
ax.tick_params(which='major', length=15, width=1)
ax.tick_params(which='minor', length=8, width=0.5)
ax.plot(label='Зависимость напряжения от времени')
ax.legend('V(t)')
plt.text(450, 2.5, "Время зарядки конденсатора:")
plt.text(750, 2.5, max_time)
plt.text(450, 2, "Время разрядки конденсатора:")
plt.text(750, 2, time)
fig.set_figwidth(10)
fig.savefig("plt.svg")

plt.show()