import requests
import time
import os
import sys
from datetime import datetime, timedelta

access_token = 'your shelly access token here, get it from the shelly app'
url = 'shelly device status url here, e.g.  https://shelly-38-eu.shelly.cloud/device/status/'

sensor1_id = 'xxxxxx'   # 6-digit id's of shelly H&T sensors
sensor2_id = 'xxxxxx'   # 
sensor3_id = 'xxxxxx'   # 
sensor4_id = 'xxxxxx'   # 
sensor5_id = 'xxxxxx'   # 

time_format = "%Y-%m-%d %H:%M:%S"

def clear_screen():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # if in windows, cls instead of clear
        command = 'cls'
    os.system(command)

clear_screen()
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def fetch_data(sensor_id):
    requestdata = {'auth_key': access_token, 'id': sensor_id}
    results = requests.post(url, data=requestdata)
    device_data = results.json()

    time_data = str(device_data['data']['device_status']['_updated'])
    last_updated = datetime.strptime(time_data, time_format)
#    last_updated = last_updated + timedelta(hours=3)                                   # time in GMT by default, use this to convert to Finnish time or whatever
    last_updated = last_updated.time()                                                  # show hours only

    temperature = device_data['data']['device_status']['tmp']['value']
    humidity = device_data['data']['device_status']['hum']['value']

    battery_voltage = device_data['data']['device_status']['bat']['voltage']
#    battery_percent = device_data['data']['device_status']['bat']['value']              # battery in %, but the API constantly shows 100. Can be uncommented if they fix it.

    sensor_info = {
        "last_updated": str(last_updated),
        "temperature": str(round(temperature)),
        "humidity": str(round(humidity)),
        "battery_status": str(round(battery_voltage, 1))
#       "battery_status": str(battery_voltage) + "v (" + str(battery_percent) + "%)"
    }

    print("...")            # progress indicator
    time.sleep(1.5)         # pause because Shelly api is limited to 1 request per second
    return sensor_info

print("Fetching sensor data from the cloud...")
sensor1_data = fetch_data(sensor1_id)
sensor2_data = fetch_data(sensor2_id)
sensor3_data = fetch_data(sensor3_id)
sensor4_data = fetch_data(sensor4_id)
sensor5_data = fetch_data(sensor5_id)

with open(os.path.join(sys.path[0], "template.html"), "r") as f:
    html_page = f.read()

# replace the following strings in the html page template with the appropriate sensor readings
replaced_strings = {
    "[[sensor1_temp]]": sensor1_data['temperature'],
    "[[sensor2_temp]]": sensor2_data['temperature'],
    "[[sensor3_temp]]": sensor3_data['temperature'],
    "[[sensor4_temp]]": sensor4_data['temperature'],
    "[[sensor5_temp]]": sensor5_data['temperature'],
    "[[sensor1_hum]]": sensor1_data['humidity'],
    "[[sensor2_hum]]": sensor2_data['humidity'],
    "[[sensor3_hum]]": sensor3_data['humidity'],
    "[[sensor4_hum]]": sensor4_data['humidity'],
    "[[sensor5_hum]]": sensor5_data['humidity'],
    "[[sensor1_batt]]": sensor1_data['battery_status'],
    "[[sensor2_batt]]": sensor2_data['battery_status'],
    "[[sensor3_batt]]": sensor3_data['battery_status'],
    "[[sensor4_batt]]": sensor4_data['battery_status'],
    "[[sensor5_batt]]": sensor5_data['battery_status'],
    "[[sensor1_update]]": sensor1_data['last_updated'],
    "[[sensor2_update]]": sensor2_data['last_updated'],
    "[[sensor3_update]]": sensor3_data['last_updated'],
    "[[sensor4_update]]": sensor4_data['last_updated'],
    "[[sensor5_update]]": sensor5_data['last_updated'],
}

for key in replaced_strings:
    html_page = html_page.replace(key, replaced_strings[key], 1)


with open(os.path.join(sys.path[0], "sensors.html"), "w") as output_file:
    write = output_file.write(html_page)
    output_file.close()

print("sensors.html written")
print("\n")

def print_data(sensor_data):
    for key in sensor_data:
        print(key + ": " + sensor_data[key])
    print("\n")

print_data(sensor1_data)
print_data(sensor2_data)
print_data(sensor3_data)
print_data(sensor4_data)
print_data(sensor5_data)
