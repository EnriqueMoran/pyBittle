"""An example of creating a Bittle instance and communicate with it.

Three examples are provided, three of them consist in creating a Bittle
instance and connect to it through Bluetooth, WiFi or Serial.
If connection is sucessful, send 'khi' and 'd' commands to check whether
Bittle receives and replies to them.
"""

import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '..'))

from pyBittle import bittleManager  # noqa: E402


__author__ = "EnriqueMoran"


greet = bittleManager.Command.GREETING  # khi command
rest = bittleManager.Command.REST  # d command


def test_bluetooth(bittle):
    """Connect to Bittle through Bluetooth and send 'khi' and 'd' commands.

    Parameters:
            bittle (bittleManager.Bittle) : Bittle instance.
    """
    print("Connecting to Bittle through Bluetooth...")
    isConnected = bittle.connect_bluetooth()
    print(f"Connected: {isConnected}")
    if isConnected:
        print("Sending command: 'GREETING'...")
        bittle.send_command_bluetooth(greet)
        received = bittle.receive_msg_bluetooth()
        decoded_msg = received.decode("utf-8")
        decoded_msg = decoded_msg.replace('\r\n', '')
        print(f"Received message: {decoded_msg}, expected: k")
        time.sleep(6)
        print("Sending command: 'REST'...")
        bittle.send_command_bluetooth(rest)
        received = bittle.receive_msg_bluetooth()
        decoded_msg = received.decode("utf-8")
        decoded_msg = decoded_msg.replace('\r\n', '')
        print(f"Received message: {decoded_msg}, expected: d")
        time.sleep(5)
        print("Closing Bluetooth connection...")
        bittle.disconnect_bluetooth()
        print("Connection closed")
    else:
        print("Bittle not found")


def test_wifi(bittle):
    """Connect to Bittle through WiFi and send 'khi' and 'd' commands.

    Parameters:
            bittle (bittleManager.Bittle) : Bittle instance.
    """
    bittle.wifiManager.ip = input("Enter Bittle IP address: ")
    print("Connecting to Bittle through WiFi...")
    if bittle.has_wifi_connection():
        print(f"Bittle found, REST API address: "
              f"{bittle.wifiManager.http_address}")
        print("Sending command: 'GREETING'...")
        response = bittle.send_command_wifi(greet)
        print(f"Received message: {response}, expected: 200")
        time.sleep(6)
        print("Sending command: 'REST'...")
        response = bittle.send_command_wifi(rest)
        print(f"Received message: {response}, expected: 200")
        time.sleep(6)
        print("Connection closed")
    else:
        print("Can't connect to Bittle")

if __name__ == "__main__":
    connection = int(input("Select test (1 -> Bluetooth, 2 -> WiFi): "))
    if connection != 1 and connection != 2:
        print("Wrong value.")
    else:
        bittle = bittleManager.Bittle()
        print("Bittle instance created")
        if connection == 1:
            test_bluetooth(bittle)
        elif connection == 2:
            test_wifi(bittle)
        elif connection == 3:
            pass
    print("Bittle data:\n {!s}".format(bittle))
