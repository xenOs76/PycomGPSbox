"""Use micropyGPS library to define a GPS obj.

Gets some custom functions from settings to convert data as numeric values so
they can be ready to be packed and sent over LoRa messages.
"""
from settings import cnf
from common import sign_coord
from common import dir_to_n
from common import pgb

import machine
from machine import I2C
from micropyGPS import MicropyGPS
from micropython import const

gps_offset = cnf['gps_offset']

print("GPS: Initializing mGPS...")
GPS_TIMEOUT_SECS = 10
# init I2C to P21/P22
i2c = machine.I2C(0, mode=I2C.MASTER, pins=('P22', 'P21'))
# write to address of GPS
GPS_I2CADDR = const(0x10)
raw = bytearray(1)
i2c.writeto(GPS_I2CADDR, raw)
# create MicropyGPS instance
# gps = MicropyGPS()
gps = MicropyGPS(local_offset=gps_offset, location_formatting='dd')
# start a timer
chrono = machine.Timer.Chrono()
chrono.start()


def get_gps_data(gps, Debug):
    """Poll the GPS module and returns a dict."""
    gps_data = False
    raw = i2c.readfrom(GPS_I2CADDR, 16)
    for b in raw:
        sentence = gps.update(chr(b))
        # print("GPS: querying for valid sentence")  # verbose output
        if sentence is not None:
            if gps.satellite_data_updated() and gps.valid:
                if Debug:
                    print("GPS: updated {}, valid {}"
                          .format(gps.satellite_data_updated(), gps.valid))
                    # print("GPS: sentence {}".format(str(sentence)))
                    # print("GPS: raw i2c {}".format(str(raw)))
                gps_data = {}
                gps_data['date_s'] = gps.date_string()
                gps_data['date'] = gps.date_string('s_dmy')
                gps_data['crs'] = gps.course
                gps_data['dir'] = gps.compass_direction()
                gps_data['dir_n'] = dir_to_n(gps.compass_direction())
                gps_data['ts'] = gps.timestamp
                gps_data['lat_s'] = gps.latitude_string()
                gps_data['lat'] = sign_coord(gps.latitude)
                gps_data['lon_s'] = gps.longitude_string()
                gps_data['lon'] = sign_coord(gps.longitude)
                gps_data['spd'] = round(gps.speed[2], 1)  # km/h
                gps_data['alt'] = round(gps.altitude, 1)

    if gps_data:
        if 'lat' in gps_data and 'lon' in gps_data:
            print("GPS: lat ", gps_data['lat'], "| lon ", gps_data['lon'])
            print("GPS: spd ", gps_data['spd'], "| ts", gps_data['ts'])
            print("GPS: d ", gps_data['date'], "| alt ", gps_data['alt'])
            print("GPS: dir ", gps_data['dir'])
            if Debug:
                print("GPS: lat ", gps_data['lat_s'], "| lon ",
                      gps_data['lon_s'])
                print("GPS: dir ", gps_data['dir'], "| dir_n ",
                      gps_data['dir_n'])
                print("GPS: -------------------------------------------------")
            pgb.update_gps_data(gps_data)
        else:
            pgb.update_gps_data(False)
