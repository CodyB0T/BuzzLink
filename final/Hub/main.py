from machine import Pin, I2C, PWM
import time
from collections import OrderedDict

import ssd1306
from writer import Writer
import courier20

from rotary_irq_esp import RotaryIRQ

import network
import espnow


data = OrderedDict(
    [("Everyone", {b"\xa0\xb7\x65\x69\xb3\xa4"}), ("Cody", b"\xa0\xb7\x65\x69\xb3\xa4")]
)

keys = list(data.keys())

# esp now

net = network.WLAN(network.STA_IF)  # Or network.AP_IF
net.active(True)
net.disconnect()  # For ESP8266

e = espnow.ESPNow()
e.active(True)

for x in data["Everyone"]:
    e.add_peer(x)

# peer = b"\xa0\xb7\x65\x69\xb3\xa4"  # MAC address of peer's wifi interface
# e.add_peer(peer)  # Must add_peer() before send()

# oled

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64

time.sleep(1)

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
wri = Writer(oled, courier20)

# rotary encoder

# r = RotaryIRQ(
#     pin_num_clk=12,
#     pin_num_dt=13,
#     min_val=0,
#     max_val=len(data) - 1,
#     reverse=True,
#     range_mode=RotaryIRQ.RANGE_BOUNDED,
#     pull_up=True,
# )
r = RotaryIRQ(
    pin_num_clk=32,
    pin_num_dt=25,
    min_val=0,
    max_val=len(data) - 1,
    reverse=True,
    range_mode=RotaryIRQ.RANGE_BOUNDED,
    pull_up=True,
)

rbtn = Pin(18, Pin.IN, Pin.PULL_UP)

val_old = r.value()

l = Pin(2, Pin.OUT)

# functions


def blink():
    l.value(1)
    time.sleep(1)
    l.value(0)
    time.sleep(1)


def displayMenu(val):
    oled.fill(0)
    Writer.set_textpos(oled, 0, 0)  # verbose = False to suppress console output

    page = (val // 3) * 3
    print(page)
    s = ""

    for x in range(3):
        if page + x > len(keys) - 1:
            break
        else:
            if val % 3 == x:
                s += ">"
            if x == 2:
                s += f"{keys[page+x]}"
            else:
                s += f"{keys[page+x]}\n"
    print(s)

    wri.printstring(s)

    oled.show()


def sendScreen(val):
    oled.fill(0)
    Writer.set_textpos(oled, 20, 0)  # verbose = False to suppress console output
    wri.printstring("Sending")
    oled.show()

    if val == 0:
        for x in data["Everyone"]:
            e.send(x, "hello", False)
    else:
        e.send(data[keys[val]], "hello", False)

    time.sleep_ms(1000)
    displayMenu(0)


# main loop

displayMenu(0)

blink()

print("starting")

# sendScreen(0)

while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        print("result =", val_new)
        displayMenu(val_new)

    if rbtn.value() == 0:
        print("push")
        sendScreen(val_new)

    time.sleep_ms(50)
