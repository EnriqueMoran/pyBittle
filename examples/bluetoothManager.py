"""An example of Connecting to Bittle using BluetoothManager.

Create a BluetoothManager instance and search for Bittle MAC address.
If Bittle is found among avaliable paired bluetooth devices, connect to it.
If connection is sucessful, send 'khi' and 'd' commands to check whether
Bittle receives and replies to them.
"""

import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '..'))

from pyBittle import bluetoothManager  # noqa: E402


__author__ = "EnriqueMoran"


if __name__ == "__main__":
    btManager = bluetoothManager.BluetoothManager()  # Create bluetoothManager
    print(f"Searching for Bittle in paired devices...")
    name, addr = btManager.initialize_name_and_address()  # Get name and addr
    if name and addr:
        print(f"Bittle found, name: {name}, address: {addr}")
        print("Connecting to Bittle...")
        connected = btManager.connect()  # Connect to Bittle
        print(f"Connected: {connected}")
        if connected:
            print("Sending message: 'khi'...")
            btManager.sendMsg("khi")
            received = btManager.recvMsg()
            decoded_msg = received.decode("utf-8")
            decoded_msg = decoded_msg.replace('\r\n', '')
            print(f"Received message: {decoded_msg}, expected: k")
            time.sleep(6)
            print("Sending message: 'd'...")
            btManager.sendMsg("d")
            received = btManager.recvMsg()
            decoded_msg = received.decode("utf-8")
            decoded_msg = decoded_msg.replace('\r\n', '')
            print(f"Received message: {decoded_msg}, expected: d")
            time.sleep(5)
            print("Closing connection...")
            btManager.closeConnection()  # Close connection
            print("Connection closed")
    else:  # Bittle not found in paired and avaliable devices
        print("Bittle not found!")
