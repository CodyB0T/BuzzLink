from machine import Pin, I2C
import time

import ssd1306
from writer import Writer
import courier20

from rotary_irq_esp import RotaryIRQ


rbtn = Pin(27, Pin.IN, Pin.PULL_UP)
btn = Pin(0, Pin.IN)


data = {
    "Cody": b"\x02\x42\xac\x11\x00\xef",
    "Derek": b"\x1a\x2b\x3c\x4d\x5e\x6f",
    "Basement": b"\x8c\xa1\x63\x7f\xd2\x09",
    "Everyone": {
        b"\x02\x42\xac\x11\x00\xef",
        b"\x1a\x2b\x3c\x4d\x5e\x6f",
        b"\x8c\xa1\x63\x7f\xd2\x09",
    },
}


# oled

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# rotary encoder

r = RotaryIRQ(
    pin_num_clk=12,
    pin_num_dt=14,
    min_val=0,
    max_val=3,
    reverse=False,
    range_mode=RotaryIRQ.RANGE_WRAP,
)

val_old = r.value()

# functions


def displayMenu(val):
    oled.fill(0)

    wri = Writer(oled, courier20)

    Writer.set_textpos(oled, 0, 0)  # verbose = False to suppress console output

    bounds = findBounds(val)

    keys = list(data.keys())

    wri.printstring(f"{keys[bounds[0]]}\n>{keys[bounds[1]]}\n{keys[bounds[2]]}")

    oled.show()


def findBounds(mid):
    up = 0
    down = 0

    if mid == len(data) - 1:
        up = mid - 1
        down = 0
    elif mid == 0:
        up = len(data) - 1
        down = mid + 1
    else:
        up = mid - 1
        down = mid + 1

    return [up, mid, down]


# main loop

displayMenu(0)
print("starting")
while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        print("result =", val_new)
        displayMenu(val_new)

    if rbtn.value() == 0:
        print("push")
        pass

    time.sleep_ms(50)
