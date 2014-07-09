# This program is designed to run on a Raspberry Pi as a based UKHASnet node minus the radio transmitter
# Work is being done to implement an RFM69 circuit to this node with software to follow
# This script is designed to use a DHT22 with Adafruit's DHT library

#!/usr/bin/python

import subprocess
import re
import sys
import time
import urllib
import httplib

node_id = "NORB1"
position = "53.5303053,-2.7170677"
repeats = 1
repeat_count = 0
letter_identifier = 97
path = "[" + node_id + "]"
packet = ""
origin = node_id

def upload_data(line):
    params = urllib.urlencode({'origin': origin, 'data': line})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("www.ukhas.net:80")
    conn.request("POST", "/api/upload", params, headers)
    response = conn.getresponse()
    if response.status != 200:
        print 'Upload Failed: ' + response.read()
    data = response.read()
    conn.close()
    return


def generate_packet(current_repeat, temp, hum):
    time.sleep(60)
    global letter_identifier
    if letter_identifier == 97:
        packet = str(repeats - current_repeat) + chr(letter_identifier) + "L" + str(position) + "T" + str(temp) + "H" + str(hum) + path
    else:
        packet = str(repeats - current_repeat) + chr(letter_identifier) + "T" + str(temp) + "H" + str(hum) + path

    print packet

    if letter_identifier == 122:
        letter_identifier = 98
    else:
        letter_identifier += 1
    
    return packet


# Continuously append data
while True:
    # Run the DHT program to get the humidity and temperature readings!

    output = subprocess.check_output(["./Adafruit_DHT", "22", "4"])
    print output
    matches = re.search("Temp =\s+([0-9.]+)", output)
    if not matches:
        time.sleep(3)
        continue
    temp = float(matches.group(1))
  
    # search for humidity printout
    matches = re.search("Hum =\s+([0-9.]+)", output)
    if not matches:
        time.sleep(3)
        continue
    humidity = int(float(matches.group(1)))

    for repeat_count in range(0, repeats):
        packet = generate_packet(repeat_count, temp, humidity)
        upload_data(packet)
        if repeats - repeat_count == 1:
            break


