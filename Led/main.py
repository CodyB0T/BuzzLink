import machine
import time

l = machine.Pin(2, machine.Pin.OUT)

while True:
    l.value(1)
    time.sleep(1)
    l.value(0)
    time.sleep(1)