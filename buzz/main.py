import machine
import time

p26 = machine.Pin(26, machine.Pin.OUT)
beeper = machine.PWM(p26, freq=1047, duty=512)
time.sleep(0.5)
beeper.deinit()
print("done")
