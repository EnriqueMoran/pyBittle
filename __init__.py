import pyBittle

"""
pyBittle - a library to connect to Bittle, manage and control its behaviour.

Classes:

Functions:
"""


__author__ = "EnriqueMoran"

__version__ = "v0.1"



if __name__ == "__main__":
    btManager = pyBittle.BluetoothManager()
    print(btManager.initialize_name_address_port())