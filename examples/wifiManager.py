"""An example of Connecting to Bittle using WiFi.

Create a WifiManager instance and check wether there is connection to REST
API. If there is connection, send 'khi' and 'd' commands to check whether
Bittle receives and replies to them.
"""

import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '..'))

from pyBittle import wifiManager  # noqa: E402


__author__ = "EnriqueMoran"


if __name__ == "__main__":
    wifiManager = wifiManager.WifiManager()  # Create wifiManager
    ip = input("Enter Bittle IP address: ")  # Ask for Bittle IP address
    wifiManager.ip = ip
    print("Searching for Bittle connetion...")
    if wifiManager.has_connection():
        print(f"Bittle found, REST API address: {wifiManager.http_address}")
        print("Sending message: 'khi'...")
        response = wifiManager.send_msg("khi")
        print(f"Received message: {response}, expected: 200")
        time.sleep(6)
        print("Sending message: 'd'...")
        response = wifiManager.send_msg("d")
        print(f"Received message: {response}, expected: 200")
        time.sleep(5)
        print("Connection closed")
    else:  # Can't connect to REST API
        print("Bittle not found!")
