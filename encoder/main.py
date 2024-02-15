import time
import machine
from rotary_irq_esp import RotaryIRQ

r = RotaryIRQ(pin_num_clk=12, 
              pin_num_dt=13, 
              min_val=0, 
              max_val=5, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP,
              pull_up=True)
              
val_old = r.value()
while True:
    val_new = r.value()
    
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
        
    time.sleep_ms(50)

# a = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
# b = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

# while True:
#     # print(a.value(),b.value())
#     if

#     time.sleep(.005)