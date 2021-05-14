"""This module manages Serial communication.

SerialManager allows sending commands to Bittle through Serial.
"""

import serial
import serial.tools.list_ports

__author__ = "EnriqueMoran"


class SerialManager:
    """Main class to manage Serial connection.

    Attributes
    ----------
    port : str
        Serial communication port.
    baudrate : int
        Baud rate.
    timeout : int
        Serial communication timeout (seconds).
    parity : int
        Serial communication parity (possible values: none, odd, even).
    serial : serial.Serial
        Serial communication instance.

    Methods
    -------
    initialize():
        Sets serial communication parameters. If any of the parameters is
        updated after initialization, this method must be called to apply
        the changes.
    discover_port():
        Searches among avaliable communication ports the one associated
        to CH340 USB driver, which is used by Bittle.
    connect():
        Starts serial communication. Return wether connection was achieved.
    close_connection():
        Closes serial communication.
    send_msg(msg):
        Sends a message to Bittle.
    recv_msg():
        Returns received message from Bittle (byte).
    """

    def __init__(self):
        self._port = "COM1"
        self._baudrate = 115200
        self._timeout = 5
        self._parity = serial.PARITY_NONE
        self.serial = serial.Serial()

    def __del__(self):
        self.serial.close()

    def __repr__(self):
        return f"SerialManager - port: {self.port}, baudrate: " \
               f"{self.baudrate}, timeout: {self.timeout}, parity: " \
               f"{self.parity}"

    def __str__(self):
        return f"SerialManager - port: {self.port}, baudrate: " \
               f"{self.baudrate}, timeout: {self.timeout}"

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        if isinstance(new_port, str) and new_port:
            self._port = new_port
        else:
            raise TypeError("Port must be non empty str.")

    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, new_baudrate):
        if isinstance(new_baudrate, int) and new_baudrate > 0:
            self._baudrate = new_baudrate
        else:
            raise TypeError("Baudrate type must be int, greater than 0.")

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout):
        if isinstance(new_timeout, int) and new_timeout >= 0:
            self._timeout = new_timeout
        else:
            raise TypeError("Timeout must be positive int.")

    @property
    def parity(self):
        return self._parity

    @parity.setter
    def parity(self, new_parity):
        if isinstance(new_parity, str) and new_port:
            if new_parity.lower().replace(' ', '') == 'none':
                self._parity = serial.PARITY_NONE
            elif new_parity.lower().replace(' ', '') == 'odd':
                self._parity = serial.PARITY_ODD
            elif new_parity.lower().replace(' ', '') == 'even':
                self._parity = serial.PARITY_EVEN
            else:
                raise TypeError("Parity value be 'none', 'odd' or 'even'.")
        else:
            raise TypeError("Parity must be non empty str.")

    def initialize(self):
        """Sets serial communication parameters.
        """
        self.serial.baudrate = self.baudrate
        self.serial.port = self.port
        self.serial.timeout = self.timeout
        self.serial.parity = self.parity

    def discover_port(self):
        """Search among avaliable communication ports the one associated
        to CH340 USB driver, which is used by Bittle; if found, set self.port
        with its value. Returns True if found, False otherwise.
        """
        res = False
        for port in serial.tools.list_ports.comports():
            if "CH340" in port.description:
                self.port = port.device
                res = True
                break
        return res

    def connect(self):
        """Connects to Bittle and wait until full response is given
        (response will contain "Finished! at the end").
        Returns:
            res (bool) : True if connected successfully, False otherwise.
        """
        res = False
        self.serial.open()
        while True:
            data = self.recv_msg()
            if len(data) == 0:
                    break
            elif b"Finished!" in data:
                res = True
                self.recv_msg()  # Remove last blank line
                break
        return res


    def close_connection(self):
        """Closes serial communication.
        """
        self.serial.close()

    def send_msg(self, msg):
        """Sends a message to Bittle.
        """
        if isinstance(msg, str) and msg:
            self.serial.write(msg.encode())
        else:
            raise TypeError("Message must be non empty str.")

    def recv_msg(self):
        """Reads a serial data line (till '\n' character).

        Returns:
            data (byte) : Received data.
        """
        return self.serial.readline()
