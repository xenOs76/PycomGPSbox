"""Define variables to be used application wide."""
cnf = {}

# Verbose output
Debug = False
cnf["debug"] = Debug

# TTN keys - ABP device
lora_enabled = True
cnf["lora_enabled"] = lora_enabled

lora_keys = {}
lora_keys["dev_addr"] = 'XXXXXXXX'
lora_keys["nwk_swkey"] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
lora_keys["app_swkey"] = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
cnf['lora_keys'] = lora_keys

# mGPS_offset, Timezone Difference to UTC
# mGPS_offset = 0 means UTC
mGPS_offset = 0
cnf['gps_offset'] = mGPS_offset

# async functions intervals for LoRa and GPS triggers
gps_delay_ms = 1000
cnf['gps_delay_ms'] = gps_delay_ms

lora_delay_ms = 20000
cnf['lora_delay_ms'] = lora_delay_ms
