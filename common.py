"""Common functions."""
from settings import cnf

import ustruct
import time

gps_delay = cnf['gps_delay_ms']
lora_delay = cnf['lora_delay_ms']
lora_enabled = cnf['lora_enabled']


def sign_coord(coord):
    """Get a list of coordinates and returns a signed value."""
    # es:
    # Buenos Aires: 34.6037° S, 58.3816° W
    # ba_lat = ["34.6037", "S"]
    # ba_lon = ["58.3816", "W"]
    # s_lat = sign_coord(ba_lat) # outputs -34.6037
    # s_lon = sign_coord(ba_lon) # outputs -58.3816

    deg = float(coord[0])
    card = str(coord[1])
    if deg > 0 and (card == 'S' or card == 'W'):
        deg = -abs(deg)
    return deg


def dir_to_n(dir_str):
    """Convert a string containing cardinal points to a number."""
    cards = {'N': 1, 'S': 2, 'E': 3, 'W': 4}
    num_str = ''
    for char in dir_str:
        num_str += str(cards[char])
    card_n = int(num_str)
    return card_n


class Pgb:
    """Pgb: Pycom GPS box class."""

    def __init__(self):
        """Init function: defaults."""
        self.gps_data = False
        self.gps_delay_ms = 5000
        self.gps_timeout = 5000
        self.lora_enabled = False
        self.lora_timer = False
        self.lora_payload = False
        self.lora_delay_ms = 30000
        self.lora_counter = 0

    def update_gps_data(self, data_dict):
        """Update method to add/check gps data values.

        pgb.update_gps_data(dict)
        to add valid data from GPS hardware to the object

        pgb.update_gps_data(False)
        to acknowledge we don't have valid data from the GPS hardware atm.
        """
        if data_dict:
            self.gps_data = data_dict
            self.gps_date = data_dict['date']
            self.gps_date_s = data_dict['date_s']
            self.gps_dir = data_dict['dir']
            self.gps_dir_n = data_dict['dir_n']
            self.gps_ts = data_dict['ts']
            self.gps_lat = data_dict['lat']
            self.gps_lat_s = data_dict['lat_s']
            self.gps_lon = data_dict['lon']
            self.gps_lon_s = data_dict['lon_s']
            self.gps_speed = data_dict['spd']
            self.gps_alt = data_dict['alt']
        else:
            self.gps_data = False

    def update_gps_delay(self, delay_ms):
        """Set time interval for triggered polling."""
        self.gps_delay_ms = delay_ms

    def enable_lora(self, v):
        """Enable or disable LoRa functions and triggers AT BOOT."""
        if v:
            self.lora_enabled = True
        else:
            self.lora_enabled = False

    def update_lora_delay(self, delay_ms):
        """Set time interval for triggered polling."""
        self.lora_delay_ms = delay_ms

    def update_lora_timer(self, status):
        """Update timer status.

        If "True", the interval from previous message expired and is possible
        to send a new one, so we reset payload's value and increase counter.
        To be used after a successfully sent message.
        """
        if status:
            self.lora_timer = True
            self.lora_payload = False
        else:
            self.lora_timer = False

    def reset_lora_payload(self):
        """Reset LoRa payload value."""
        self.lora_payload = False

    def update_lora_counter(self):
        """Increase lora_counter."""
        counter = self.lora_counter
        self.lora_counter = counter + 1
        print("Lora: counter updated: {}".format(self.lora_counter))

    def lora_pack_payload(self):
        """Pack GPS data as a TTN payload.

        References to pack the data:
        https://www.thethingsnetwork.org/docs/devices/bytes.html
        https://docs.python.org/3/library/struct.html?highlight=struct
        https://docs.micropython.org/en/latest/library/ustruct.html?highlight=ustruct
        https://en.wikipedia.org/wiki/C_data_types

        The ts points to the timezone specified by the gps_offset value.
        """
        if self.lora_timer:
            lat = self.gps_lat  # C: float, 4 bytes
            lon = self.gps_lon  # C: float, 4 bytes
            alt = int(self.gps_alt * 10)  # C: unsigned short, 2 bytes
            speed = int(self.gps_speed * 10)  # C: unsigned short, 2 bytes
            dir = int(self.gps_dir_n)  # max 4321, C: unsignes short, 2 bytes

            date = self.gps_date
            date_l = date.split('/')
            Y = int(date_l[2])+2000
            M = int(date_l[1])
            D = int(date_l[0])
            h = int(self.gps_ts[0])
            m = int(self.gps_ts[1])
            s = int(self.gps_ts[2])
            t_tuple = (Y, M, D, h, m, s, 0, 0)
            ts = time.mktime(t_tuple)  # C: unsigned long, 4 bytes
            payload = ustruct.pack('<ffHHHL',
                                   lat, lon, alt,
                                   speed, dir, ts)
            self.lora_payload = payload


pgb = Pgb()
pgb.update_gps_delay(gps_delay)
pgb.update_lora_delay(lora_delay)
