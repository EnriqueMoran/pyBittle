"""This module manages Bluetooth connection.

BluetoothManager allows finding Bittle's physical address, connecting to
Bittle, sending and receiving messages from it.
"""

import subprocess
import time

import bluetooth
import serial.tools.list_ports


__author__ = "EnriqueMoran"


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
    discovery_timeout : int
        Time for discovery Bluetooth devices (seconds).
    recv_timeout : int
        Socket timeout for receiving messages (seconds).
    socket : bluetooth.BluetoothSocket
        Socket for Bluetooth connection.

    Methods
    -------
    initialize_name_address_port(get_first_bittle=True):
        Finds and sets Bittle's device name and MAC address.
    get_paired_devices(flush_cache=True, lookup_names=True):
        Returns avaliable paired devices.
    connect():
        Connects to Bittle.
    sendMsg(msg):
        Sends a message to Bittle.
    recvMsg(buffer_size=1024):
        Returns received message from Bittle.
    closeConnection():
        Closes connection with Bittle.
    """

    def __init__(self, name="", port=1, discovery_timeout=8, recv_timeout=10):
        self._name = name
        self._address = ""
        self._port = port
        self._discovery_timeout = discovery_timeout
        self._recv_timeout = recv_timeout
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def __del__(self):
        self.socket.close()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and new_name:
            self._name = new_name
        else:
            raise TypeError("Name must be non empty str.")

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        if isinstance(new_address, str) and new_address:
            self._address = new_address
        else:
            raise TypeError("Address must be non empty str.")

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        if isinstance(new_port, int) and new_port > 0:
            self._port = new_port
        else:
            raise TypeError("Port type must be int, greater than 0.")

    @property
    def discovery_timeout(self):
        return self._discovery_timeout

    @discovery_timeout.setter
    def discovery_timeout(self, new_timeout):
        if isinstance(new_timeout, int) and new_timeout > 0:
            self._discovery_timeout = new_timeout
        else:
            raise TypeError("New timeout type must be int, greater than 0.")

    @property
    def recv_timeout(self):
        return self._recv_timeout

    @recv_timeout.setter
    def recv_timeout(self, new_timeout):
        if isinstance(new_timeout, int) and new_timeout > 0:
            self._recv_timeout = new_timeout
        else:
            raise TypeError("New timeout type must be int, greater than 0.")

    def initialize_name_address_port(self, get_first_bittle=True):
        """Sets self._name and self._address values by searching
        among paired devices and returns its values.

        Parameters:
            get_first_bittle (bool): If True, it will search for the first
            "BittleSPP" occurrence; otherwise will search for self._name
            ocurrence (full name must be stored in self._name:
            BittleSPP-XXXXXX). If is set to False but there is no valid
            self._name (empty), it will work as if was set to True.

        Returns:
            name (str) : Found name, None if not found.
            address (str) : Found address, None if not found.
        """
        if isinstance(get_first_bittle, bool):
            pass
        else:
            raise TypeError("Value type must be bool.")

        search_name = self.name if not get_first_bittle and self.name else \
            "BittleSPP"
        paired_devices = self.get_paired_devices(self.discovery_timeout)

        for address, name in list(paired_devices):
            if search_name in name:
                self.name = name
                self.address = address
                return self.name, self.address
        else:  # Bittle name not found, return (None, None, None)
            return None, None

    def get_paired_devices(self, flush_cache=True, lookup_names=True):
        """Returns dict {MAC address : device name} with paired devices.

        Check bluetooth.discover_devices documentation for more info.
        """
        return bluetooth.discover_devices(duration=self.discovery_timeout,
                                          flush_cache=flush_cache,
                                          lookup_names=lookup_names)

    def connect(self):
        """Connects to Bittle.

        Connects to Bittle and wait until full response is given
        (response will contain "Finished! at the end").
        Once its connected, set self.socket's timeout to self._recv_timeout.

        Returns:
            res (bool) : True if connected succesfully, False otherwise.
        """
        res = False
        try:
            self.socket.connect((self.address, self.port))
            self.socket.settimeout(self._recv_timeout)
            while True:
                data = self.socket.recv(1024)  # TODO: adjust buffer size
                if len(data) == 0:
                    break
                elif b"Finished!" in data:
                    res = True
                    break
        except:
            pass
        if not res:  # Reset socket
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        return res

    def sendMsg(self, msg):
        """Sends a message to Bittle.

        Parameters:
            msg (str) : Message to send.
        """
        if isinstance(msg, str) and msg:
            self.socket.send(msg)
        else:
            raise TypeError("Message must be non empty str.")

    def recvMsg(self, buffer_size=1024):
        """Receives a message from Bittle.

        Parameters:
            buffer_size (int) : Buffer size.

        Returns:
            data (bytes) : Received data.
        """
        data = b''
        if isinstance(buffer_size, int) and buffer_size > 0:
            try:
                data = self.socket.recv(buffer_size)
            except socket.error:
                raise socket.error("Receiving message failed: connection\
                                    timed out.")
        else:
            raise TypeError("Buffer size must be int, greater than zero.")
        return data

    def closeConnection(self):
        """Closes connection.
        """
        self.socket.close()
