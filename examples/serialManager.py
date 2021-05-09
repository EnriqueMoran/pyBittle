"""An example of Connecting to Bittle using SerialManager.

Create a SerialManager instance and search for Bittle communication
port. If port found, connect to it.
If connection is successful, send 'ksit' and 'd' commands to check
wether Bittle receives and replies to them.
"""

import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '..'))

from pyBittle import serialManager  # noqa: E402


__author__ = "EnriqueMoran"


if __name__ == "__main__":
    srManager = serialManager.SerialManager()  # Create serialManager
    print(f"Searching for Bittle communication port...")
    port_found = srManager.discover_port()
    if not port_found:
        srManager.port = 'COM7'  # Set port manually
    srManager.initialize()
    print("Connecting to Bittle...")
    connected = srManager.connect()  # Connect to Bittle
    print(f"Connected: {connected}")
    if connected:
        print("Sending message: 'ksit'...")
        srManager.send_msg('ksit')
        received = srManager.recv_msg()
        decoded_msg = received.decode("utf-8")
        decoded_msg = decoded_msg.replace('\r\n', '')
        print(f"Received message: {decoded_msg}, expected: k")
        time.sleep(6)
        srManager.send_msg('d')
        received = srManager.recv_msg()
        decoded_msg = received.decode("utf-8")
        decoded_msg = decoded_msg.replace('\r\n', '')
        print(f"Received message: {decoded_msg}, expected: d")
        time.sleep(5)
        print("Closing connection...")
        srManager.close_connection()
        print("Connection closed")
    else:
        print("Bittle not found!")
