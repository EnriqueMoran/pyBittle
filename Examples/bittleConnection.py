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

import pyBittle  # noqa: E402


__author__ = "EnriqueMoran"


greet = pyBittle.Command.GREETING  # khi command
rest = pyBittle.Command.REST  # d command


def testBluetooth(bittle):
    """Connect to Bittle through Bluetooth and send 'khi' and 'd' commands.

    Parameters:
            bittle (pyBittle.Bittle) : Bittle instance.
    """
    print("Connecting to Bittle through Bluetooth...")
    isConnected = bittle.connectBluetooth()
    print(f"Connected: {isConnected}")
    if isConnected:
        bittle.sendCommandBluetooth(greet)
        received = bittle.receiveMsgBluetooth()
        decoded_msg = received.decode("utf-8")
        decoded_msg = decoded_msg.replace('\r\n', '')
        print(f"Received message: {decoded_msg}, expected: k")
        time.sleep(6)
        print("Sending message: 'd'...")
        bittle.sendCommandBluetooth(rest)
        received = bittle.receiveMsgBluetooth()
        decoded_msg = received.decode("utf-8")
        decoded_msg = decoded_msg.replace('\r\n', '')
        print(f"Received message: {decoded_msg}, expected: d")
        time.sleep(5)
        print("Closing Bluetooth connection...")
        bittle.disconnectBluetooth()
        print("Connection closed")

if __name__ == "__main__":
    connection = 1  # 1 -> Bluetooth, 2 -> WiFi, 3 -> Serial
    bittle = pyBittle.Bittle()
    print("Bittle instance created")
    if connection == 1:
        testBluetooth(bittle)
    elif connection == 2:
        pass
    elif connection == 3:
        pass
    print("Bittle data:\n {!s}".format(bittle))