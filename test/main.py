from machine import Pin, I2C, PWM
import time
from collections import OrderedDict

import ssd1306
from writer import Writer
import courier20

from rotary_irq_esp import RotaryIRQ


rbtn = Pin(27, Pin.IN, Pin.PULL_UP)
btn = Pin(0, Pin.IN)


data = OrderedDict([
    ("everyone", 0),
    ("Cody", 1),
    ("Basement", 2),
    ("Derek", 3),
    ("Codyx", 4),
    ("Basementx", 5),
    ("Derekx", 6)
])




# oled

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64

time.sleep(1)

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
wri = Writer(oled, courier20)

# rotary encoder

r = RotaryIRQ(
    pin_num_clk=12,
    pin_num_dt=13,
    min_val=0,
    max_val=len(data)-1,
    reverse=False,
    range_mode=RotaryIRQ.RANGE_BOUNDED,
    pull_up=True
)

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

  keys = list(data.keys())
  page = (val//3) * 3
  print(page)
  s = ""

  for x in range(3):
    if page+x > len(keys)-1:
      break
    else:
      if val%3 == x:
        s += '>'
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
