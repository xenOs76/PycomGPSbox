#!/usr/bin/python3
"""Set a TTN client.

mosquitto_sub cli:
mosquitto_sub -h eu.thethings.network -d -t '#' -u app_id -P ttn-KEY -v
"""


import time
import ttn
import json


app_id = 'os76-lopy-dev'
access_key = 'ttn-account-XXXXXXXXXXXXXXXXXXXXXXXXXXX'
ttn_mqtt = 'eu.thethings.network'
discovery_addr = "discovery.thethings.network:1900"


def connect_callback(res, client):
    """Connect callback."""
    if res:
        print("Connected to Mqtt")


def uplink_callback(msg, client):
    """Print received messages."""
    print(msg)
    print("------------------------")
    dev = msg.dev_id
    count = msg.counter
    fields = json.loads(msg.payload_fields)
    print("Received uplink {} from dev {}".format(count, dev))
    print("Payload fields:".format(type(fields)))


handler = ttn.HandlerClient(app_id, access_key)
# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_connect_callback(connect_callback)
mqtt_client.set_uplink_callback(uplink_callback)

mqtt_client.connect()
time.sleep(60)
mqtt_client.close()

"""
# using application manager client
app_client = handler.application()
my_app = app_client.get()
print(my_app)

my_devices = app_client.devices()
print(my_devices)
"""
