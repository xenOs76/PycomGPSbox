"""Use GPS and LoRa libaries to send position data."""
from settings import cnf
from common import pgb
from lora_ABP import lora_send
from mgps import gps, get_gps_data


import utime
import pycom
import uasyncio as asyncio
from machine import WDT


Debug = cnf['debug']
wdt_timeout = cnf['gps_delay_ms'] * 5
wdt = WDT(timeout=wdt_timeout)
lora_start = cnf["lora_enabled"]

pgb.enable_lora(lora_start)


async def get_async_gps_data(gps, pgb, Debug):
    """Look for valid GPS data and send them over LoRa."""
    while True:
        await asyncio.sleep_ms(pgb.gps_delay_ms)
        # print("GPS: querying hardware")  # verbose ouptut
        wdt.feed()
        get_gps_data(gps, Debug)
        if pgb.gps_data:
            if Debug:
                print("GPS: async update available")
            if pgb.lora_enabled and pgb.lora_timer:
                lora_send(Debug)


if pgb.lora_enabled:
    async def lora_async_timer(pgb, Debug):
        """Set a timer to delay LoRa messages."""
        while True:
            await asyncio.sleep_ms(pgb.lora_delay_ms)
            if Debug:
                print("LoRa: async timer")
            pgb.update_lora_timer(True)


loop = asyncio.get_event_loop()
loop.create_task(get_async_gps_data(gps, pgb, Debug))
if pgb.lora_enabled:
    loop.create_task(lora_async_timer(pgb, Debug))
loop.run_forever()
