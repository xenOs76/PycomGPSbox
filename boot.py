"""Boot file: executed at boot only."""
from machine import UART
import machine
import os
import pycom
from network import WLAN
from network import Bluetooth

# Heartbeat LED
pycom.heartbeat(False)

# WIFI + WIFI AP at boot
print("Boot: disabling WIFI")
pycom.wifi_on_boot(False)
wlan = WLAN()
wlan.deinit()

# Bluetooth
print("Boot: disabling Bluetooth")
bluetooth = Bluetooth()
bluetooth.deinit()

uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('main.py')
