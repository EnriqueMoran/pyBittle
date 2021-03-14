"""
This module manages Bluetooth connection.

Classes:

Functions:
"""

import subprocess

import bluetooth
import serial.tools.list_ports  #pyserial, pybluez borrar


__author__ = "EnriqueMoran"

__version__ = "v0.1"


class BluetoothManager():
    """Main class to manage Bluetooth connection.

    Attributes
    ----------
    name : str
        Bittle device name (by default its BittleSPP-XXXXXX).
    address : str
        Bittle device MAC address.
    port : int
        Communication port.
    discovery_duration : int
        Time for discovery Bluetooth devices.
    """

    def __init__(self, name="", discovery_duration=8):
        self._name = name
        self._address = ""
        self._port = -1
        self.discovery_duration = discovery_duration

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str):
            self._name = new_name
        else:
            raise TypeError("Name type must be str.")

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        if isinstance(new_address, str):
            self._address = new_address
        else:
            raise TypeError("Address type must be str.")

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        if isinstance(new_address, int) and new_address > 0:
            self._address = new_address
        else:
            raise TypeError("Address type must be int, greater than 0.")

    def initialize_name_address_port(self, get_first_bittle=True):
        """Sets self._name, self._address and self._port values by searching
        among paired devices and returns them.

        Parameters:
            get_first_bittle (bool): If True, it will search for the first
            "BittleSPP" occurrence; otherwise will search for self._name
            ocurrence (full name must be stored in self._name). If is set to
            False but there is no valid self._name, it will work as if was set
            to True.

        Returns:
            name (str) : Found name, None if not found
            address (str) : Found address, None if not found
            port (int) : Found port, None if not found
        """
        search_name = self.name if not get_first_bittle and self.name else \
            "BittleSPP"
        res_name = None
        res_addr = None
        res_port = None
        res_none = False  # If True, return not found (None, None, None)
        paired_devices = self.get_paired_devices(self.discovery_duration)

        for address, name in list(paired_devices):
            if search_name in name:
                res_name = name
                res_addr = address
                break
        else:  # Bittle name not found, return (None, None, None)
            res_none = True

        com_ports = list(serial.tools.list_ports.comports())
        res_none = res_none or len(com_ports) <= 0  # Are there COM ports?
        addr = address.replace(':', "")

        for com, _, hwenu in com_ports:
            if addr in hwenu:  # All needed data found
                res_port = int(com.replace("COM", ""))
                break
        else:  # Connection COM port not found
            res_none = True

        if res_none:
            return None, None, None
        else:
            self.name = res_name
            self.address = res_addr
            self.port = res_port
            return res_name, res_addr, res_port

    def get_paired_devices(self, duration=8, flush_cache=True,
                           lookup_names=True):
        """Returns dict {MAC address : device name} with paired devices.

        Check bluetooth.discover_devices documentation for more info.
        """
        return bluetooth.discover_devices(duration=duration,
                                          flush_cache=flush_cache,
                                          lookup_names=lookup_names)
