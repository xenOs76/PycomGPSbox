# Pycom GPS box

**Pycom GPS box** tries to get some useful data from a [Lopy4](https://docs.pycom.io/gettingstarted/connection/lopy4/) and a [Pytrack](https://docs.pycom.io/datasheets/boards/pytrack/) board.

It is written in [MicroPython](https://micropython.org/) and takes advantage of [microGPS](https://github.com/inmcm/micropyGPS), [micropython-async](https://github.com/peterhinch/micropython-async) and [Pycom's LoRa code](https://docs.pycom.io/firmwareapi/pycom/network/lora/) to be able to send GPS data as a **LoRaWAN** payload over [The Things Network](https://www.thethingsnetwork.org/).

It provides a decoder function to use on **TTN**'s backend to be able to read the payload.   
Once decoded, the payload will return a JSON string like the following:

```JSON
{
  "gps_data": {
    "alt": "606.9",
    "dir": "NE",
    "lat": "47.27497",
    "lon": "11.41830",
    "speed": "0.0",
    "ts": 1573717150
  }
}
```
The code tries to squeeze payload's size as much as it can using MicroPython's [ustruct](https://docs.micropython.org/en/latest/library/ustruct.html) `pack` and `unpack` functions on Python's side as well as some bytes shifting on Javascript's side.    
The `async` functions enable to set two different intervals to poll the GPS module and send messages over **LoRaWAN**.

A more advanced example of `uasyncio` and GPS polling can be found between [micropython-async's examples](https://github.com/peterhinch/micropython-async/tree/master/gps).

The `settings_sample.py` provides an example of configuration. It requires the data of a TTN's device configured as ABP to be filled up. The file can then be renamed as `settings.py`.       

The [Links](/Links.md) file provides a list of references that made writing the code a quick, pleasant, journey for a wannabe Devops.    
