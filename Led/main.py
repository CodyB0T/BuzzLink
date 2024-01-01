import machine
import time

l = machine.Pin(14, machine.Pin.OUT)

x = 0

while True:
    l.value(0)
    time.sleep(1)
    l.value(1)
    time.sleep(1)
    x = x + 1
    print(x)
