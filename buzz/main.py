import machine
import time

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

p26 = machine.Pin(23, machine.Pin.OUT)
beeper = machine.PWM(p26, freq=1047, duty=512)
btn = machine.Pin(0, machine.Pin.IN)
beeper.duty(0)

while True:
    print(btn.value())
    if(btn.value() == 0):
        beeper.duty(512)
    else:
        beeper.duty(0)

# time.sleep(0.5)
# beeper.deinit()
# print("done")
