import network
import espnow
import machine
import time

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()  # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

# btn
btn = machine.Pin(0, machine.Pin.IN)

# pot
pot = machine.ADC(machine.Pin(34))
pot.atten(machine.ADC.ATTN_11DB)       #Full range: 3.3v

# led
led = machine.Pin(2, machine.Pin.OUT)

# buzzer

p23 = machine.Pin(23, machine.Pin.OUT)
beeper = machine.PWM(p23, freq=1047, duty=0)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def ping(pin):

    led.value(1)

    for x in range(0,10):
        pot_value = pot.read()
        map_value = map(pot_value,0,4095,0,150)
        print(map_value, pot_value)

        beeper.duty(map_value)
        time.sleep(.1)
        beeper.duty(0)
        time.sleep(.1)
        
    beeper.duty(0)
    led.value(0)
    print("ping done")

    
btn.irq(trigger=machine.Pin.IRQ_FALLING, handler=ping)

led.value(1)
time.sleep(1)
led.value(0)

while True:

    host, msg = e.recv()
    if msg:  # msg == None if timeout in recv()
        print(host, msg)
        if msg == b"hello":
            ping(0)

