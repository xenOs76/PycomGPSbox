"""Set an object representing a TTN's LoRaWAN device configured as ABP.

Adds functions to pack the payload of the messages and send them.
"""

from settings import cnf
from common import pgb
from network import LoRa
import socket
import ubinascii
import ustruct

Debug = cnf['debug']
lora_keys = cnf['lora_keys']

if cnf['lora_enabled']:
    print("LoRa: Initializing LoRa...")

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
# create an ABP authentication params from TTN's device page:
# Device Address
dev_addr = ustruct.unpack(">l", ubinascii.unhexlify(lora_keys["dev_addr"]))[0]
# Network Session Key
nwk_swkey = ubinascii.unhexlify(lora_keys["nwk_swkey"])
# App Session Key
app_swkey = ubinascii.unhexlify(lora_keys["app_swkey"])
# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
# create a LoRa socket
ldev = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate
ldev.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
ldev.setblocking(True)


def lora_send(Debug=False):
    pgb.lora_pack_payload()
    if pgb.lora_payload and pgb.lora_timer:
        v = pgb.lora_payload
        t = ldev.send(v)
        pgb.update_lora_timer(False)
        pgb.update_lora_counter()
    count = pgb.lora_counter
    up = ustruct.unpack('<ffHHHL', v)
    print("LoRa: msg {} sent ({}s). Payload: {}".format(count, t, up))
