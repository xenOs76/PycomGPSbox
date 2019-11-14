# Pycom

* https://docs.pycom.io/firmwareapi/pycom/machine/wdt/
* https://forum.pycom.io/topic/4735/strptime/3

# GPS

* https://github.com/inmcm/micropyGPS
* https://github.com/peterhinch/micropython-async/tree/master/gps
* https://github.com/gregcope/L76micropyGPS
* https://m.wikihow.com/Write-Latitude-and-Longitude

# uasyncio

* https://github.com/peterhinch/micropython-async
* https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md#01-installing-uasyncio-on-bare-metal
* https://github.com/peterhinch/micropython-async/blob/master/i2c/i2c_esp.py

# LoRaWAN

## Micropython and LoRa
* https://docs.pycom.io/firmwareapi/pycom/network/lora/
* https://core-electronics.com.au/tutorials/encoding-and-decoding-payloads-on-the-things-network.html
* https://lemariva.com/blog/2018/10/micropython-esp32-sending-data-using-lora


## Lora payload
* https://www.thethingsnetwork.org/docs/devices/bytes.html
* https://docs.python.org/3/library/struct.html?highlight=struct
* https://docs.micropython.org/en/latest/library/ustruct.html?highlight=ustruct
* https://en.wikipedia.org/wiki/C_data_types
* https://www.programcreek.com/python/example/103662/ustruct.unpack
* https://core-electronics.com.au/tutorials/temperature-sensing-pycom-tmp36-tutorial.html
* https://www.thethingsnetwork.org/forum/t/best-practices-when-sending-gps-location-data/1242/21
* https://github.com/thesolarnomad/lora-serialization
* https://forum.core-electronics.com.au/t/s-send-data1-data2-data3-to-ttn-on-lopy4/5479/5


## TTN decode
* https://learn.adafruit.com/the-things-network-for-feather/payload-decoding
* https://core-electronics.com.au/tutorials/temperature-sensing-pycom-tmp36-tutorial.html

Example of decode function (*float* values):
* https://core-electronics.com.au/tutorials/temperature-sensing-pycom-tmp36-tutorial.html  > Decoding on TTN
* https://core-electronics.com.au/media/kbase/344/TTN-Decode-Float-Javascript.txt

```
function Decoder(bytes, port) {

  // Based on https://stackoverflow.com/a/37471538 by Ilya Bursov
  function bytesToFloat(bytes) {
    // JavaScript bitwise operators yield a 32 bits integer, not a float.
    // Assume LSB (least significant byte first).
    var bits = bytes[3]<<24 | bytes[2]<<16 | bytes[1]<<8 | bytes[0];
    var sign = (bits>>>31 === 0) ? 1.0 : -1.0;
    var e = bits>>>23 & 0xff;
    var m = (e === 0) ? (bits & 0x7fffff)<<1 : (bits & 0x7fffff) | 0x800000;
    var f = sign * m * Math.pow(2, e - 150);
    return f;
  }  

  // Test with 0082d241 for 26.3134765625
  return {
    // Take bytes 0 to 4 (not including), and convert to float:
    temp: bytesToFloat(bytes.slice(0, 4))
  };
}
```
