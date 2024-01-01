import network
import espnow
import machine
import time

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b"\xa0\xb7\x65\x69\xb3\xa4"  # MAC address of peer's wifi interface
e.add_peer(peer)  # Must add_peer() before send()

btn = machine.Pin(0, machine.Pin.IN)

while True:
    if btn.value() == 0:
        e.send(peer, "hello", False)
        print("hello")
        time.sleep(1)
