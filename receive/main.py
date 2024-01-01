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

led = machine.Pin(14, machine.Pin.OUT)

p26 = machine.Pin(26, machine.Pin.OUT)
beeper = machine.PWM(p26, freq=1047, duty=0)


def ping():
    startTime = time.ticks_ms()
    LedStartTime = time.ticks_ms()
    buzzStartTime = time.ticks_ms()

    count = 0

    led.value(1)

    while time.ticks_ms() - startTime < 2000:
        if time.ticks_ms() - LedStartTime >= 100:
            LedStartTime = time.ticks_ms()
            led.value(not led.value())
            count += 1
        if time.ticks_ms() - buzzStartTime >= 100:
            buzzStartTime = time.ticks_ms()
            if beeper.duty() == 700:
                beeper.duty(0)
            else:
                beeper.duty(700)

    led.value(0)
    beeper.duty(0)
    print("ping done")


while True:
    host, msg = e.irecv()
    if msg:  # msg == None if timeout in recv()
        print(host, msg)
        if msg == b"hello":
            msg = None
            ping()
