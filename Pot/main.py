# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, ADC, PWM
from time import sleep

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v

p26 = Pin(23, Pin.OUT)

led = Pin(2, Pin.OUT)

beeper = PWM(p26, freq=1047, duty=512)
btn = Pin(0, Pin.IN)
beeper.duty(0)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
  if btn.value() == 0:
    pot_value = pot.read()
    map_value = map(pot_value,0,4095,0,40)
    beeper.duty(map_value)
    print(map_value, pot_value)
  else:
     beeper.duty(0)
     led.value(1)
     sleep(.5)
     led.value(0)
     sleep(.5)