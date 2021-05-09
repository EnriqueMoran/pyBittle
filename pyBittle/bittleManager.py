"""Connect to Bittle, control and manage its behaviour.

bittleManager is a high level module that allows connecting to Bittle through
Bluetooth or WiFi, define Bittle's behaviour and send/receive commands to
control it.
"""

import uuid

from enum import Enum

from pyBittle.bluetoothManager import *
from pyBittle.serialManager import *
from pyBittle.wifiManager import *

__author__ = "EnriqueMoran"


class Command(Enum):
    """Defines avaliable commands.
    """
    REST = 1
    FORWARD = 2
    GYRO = 3
    LEFT = 4
    BALANCE = 5
    RIGHT = 6
    SHUTDOWN = 7
    BACKWARD = 8
    CALIBRATION = 9
    STEP = 10
    CRAWL = 11
    WALK = 12
    TROT = 13
    LOOKUP = 14
    BUTTUP = 15
    RUN = 16
    BOUND = 17
    GREETING = 18
    PUSHUP = 19
    PEE = 20
    STRETCH = 21
    SIT = 22
    ZERO = 23
    BUNNY = 24
    BACKFLIP = 25
    SLEEP = 26
    CHECKAROUND = 27


class Gait(str, Enum):
    """Defines avaliable gaits.
    """
    WALK = 'kwk'
    CRAWL = 'kcr'
    TROT = 'ktr'
    RUN = 'krn'


class Direction(str, Enum):
    """Defines avaliable movement directions.
    """
    FORWARD = 'F'
    FORWARDLEFT = 'L'
    FORWARDRIGHT = 'R'
    BACKWARD = 'B'
    BACKWARDLEFT = 'BL'
    BACKWARDRIGHT = 'BR'


class Bittle:
    """High level class that represents your Bittle.

    Attributes
    ----------
    id : uuid.UUID
        Bittle's unique id.
    bluetoothManager : BluetoothManager
        Manager for sending messages to Bittle through Bluetooth connection.
    wifiManager : WifiManager
        Manager for sending messages to Bittle through WiFi connection.
    serialManager : SerialManager
        Manager for sending messages to Bittle through Serial connection.
    gait : Gait
        Current gait.
    commands : {Command: str}
        Avaliable commands that can be sent to Bittle.

    Methods
    -------
    connect_bluetooth(get_first_bittle):
        Connects to Bittle through Bluetooth connection.
    send_command_bluetooth(command):
        Sends a command to Bittle through Bluetooth connection.
    send_msg_bluetooth(message):
        Sends a custom message to Bittle through Bluetooth connection.
    receive_msg_bluetooth(buffer_size):
        Returns received message from Bittle through Bluetooth connection.
    send_movement_bluetooth(direction):
        Sends a movement command to Bittle through Bluetooth connection.
    disconnect_bluetooth():
        Closes Bluetooth connection with Bittle.
    has_wifi_connection():
        Checks wether there is connection with REST API.
    send_command_wifi(command):
        Sends a command to Bittle through WiFi connection.
    send_msg_wifi(message):
        Sends a custom message to Bittle through WiFi connection.
    send_movement_wifi(direction):
        Sends a movement command to Bittle through WiFi connection.
    connect_serial(discover_port):
        Connects to Bittle through Serial connection.
    send_command_serial(command):
        Sends a command to Bittle through Serial connection.
    send_msg_serial(message):
        Sends a custom message to Bittle through Serial connection.
    receive_msg_serial(buffer_size):
        Returns received message from Bittle through Serial connection.
    send_movement_serial(direction):
        Sends a movement command to Bittle through Serial connection.
    disconnect_serial():
        Closes Serial connection with Bittle.
    """

    def __init__(self):
        self._id = uuid.uuid4()  # Bittle's id
        self.bluetoothManager = BluetoothManager()
        self.wifiManager = WifiManager()
        self.serialManager = SerialManager()
        self._gait = Gait.WALK  # Current gait
        self._commands = {  # Command : message to Bittle
            Command.REST: 'd',
            Command.FORWARD: 'F',
            Command.GYRO: 'g',
            Command.LEFT: 'L',
            Command.BALANCE: 'kbalance',
            Command.RIGHT: 'R',
            Command.SHUTDOWN: 'z',
            Command.BACKWARD: 'B',
            Command.CALIBRATION: 'c',
            Command.STEP: 'kvt',
            Command.CRAWL: 'kcr',
            Command.WALK: 'kwk',
            Command.TROT: 'ktr',
            Command.LOOKUP: 'klu',
            Command.BUTTUP: 'kbuttUp',
            Command.RUN: 'krn',
            Command.BOUND: 'kbd',
            Command.GREETING: 'khi',
            Command.PUSHUP: 'kpu',
            Command.PEE: 'kpee',
            Command.STRETCH: 'kstr',
            Command.SIT: 'ksit',
            Command.ZERO: 'kzero',
            Command.BUNNY: 'kbdF',
            Command.BACKFLIP: 'kbf',
            Command.SLEEP: 'kstp',
            Command.CHECKAROUND: 'kck'
        }

    def __eq__(self, other):
        return self._id == other._id

    def __str__(self):  # TODO: Complete
        return f"Bittle with id '{self._id}' Bluetooth name: " \
                f"'{self.bluetoothManager.name} ' MAC address: " \
                f"'{self.bluetoothManager.address}' " \
                f"IP address: '{self.wifiManager.ip}' " \
                f"REST API address: '{self.wifiManager.http_address}'"

    @property
    def gait(self):
        return self._gait

    @gait.setter
    def gait(self, new_gait):
        if isinstance(new_gait, Gait):
            self._gait = new_gait
        else:
            raise TypeError("New gait must be Gait type.")

    def connect_bluetooth(self, get_first_bittle=True):
        """Connects to Bittle.

        Parameters:
            get_first_bittle (bool): If True, connects to the first
            "BittleSPP" found device, otherwise connects to
            bluetoothManager.name device.

        Returns:
            res (bool) : True if connected, False otherwise.
        """
        res = False
        name, addr = self.bluetoothManager.initialize_name_and_address(
                     get_first_bittle)
        if name and addr:  # Bittle found among avaliable paired devices
            res = self.bluetoothManager.connect()
        return res

    def send_command_bluetooth(self, command):
        """Sends command to Bittle through Bluetooth connection.

        Parameters:
            command (Comand) : Command to send.
        """
        if isinstance(command, Command):
            self.bluetoothManager.send_msg(self._commands[command])
        else:
            raise TypeError("Command type must be Command.")

    def send_msg_bluetooth(self, message):
        """Sends custom message to Bittle through Bluetooth connection.

        Parameters:
            message (str) : Message to send.
        """
        if isinstance(message, str):
            self.bluetoothManager.send_msg(message)
        else:
            raise TypeError("Message type must be str.")

    def receive_msg_bluetooth(self, buffer_size=1024):
        """Receives a message from Bittle through Bluetooth connection.

        Parameters:
            buffer_size (int) : Buffer size.

        Returns:
            data (bytes) : Received data.
        """
        return self.bluetoothManager.recv_msg(buffer_size)

    def send_movement_bluetooth(self, direction):
        """Sends movement commands with current gait through Bluetooth
        connection.
        """
        if isinstance(direction, Direction):
            command = ''
            if direction in [Direction.BACKWARD, Direction.BACKWARDLEFT,
                             Direction.BACKWARDRIGHT]:
                command = 'kbk' + direction[1:]
            else:
                command = self.gait.value + direction.value
            self.send_msg_bluetooth(command)
        else:
            raise TypeError("Direction must be Direction type.")

    def disconnect_bluetooth(self):
        """Closes Bluetooth connection.
        """
        self.bluetoothManager.close_connection()

    def has_wifi_connection(self):
        """Returns True if there is connection with REST API, False otherwise.
        """
        return self.wifiManager.has_connection()

    def send_command_wifi(self, command):
        """Sends command to Bittle through WiFi connection.

        Parameters:
            command (Comand) : Command to send.

        Returns:
            res (int) : REST API response code, -1 if
            there is no connection.
        """
        if isinstance(command, Command):
            return self.wifiManager.send_msg(self._commands[command])
        else:
            raise TypeError("Command type must be Command.")

    def send_msg_wifi(self, message):
        """Sends custom message to Bittle through WiFi connection.

        Parameters:
            message (str) : Message to send.

        Returns:
            res (int) : REST API response code, -1 if
            there is no connection.
        """
        if isinstance(message, str):
            return self.wifiManager.send_msg(message)
        else:
            raise TypeError("Message type must be str.")

    def send_movement_wifi(self, direction):
        """Sends movement commands with current gait through WiFi
        connection.
        """
        if isinstance(direction, Direction):
            command = ''
            if direction in [Direction.BACKWARD, Direction.BACKWARDLEFT,
                             Direction.BACKWARDRIGHT]:
                command = 'kbk' + direction[1:]
            else:
                command = self.gait.value + direction.value
            self.send_msg_wifi(command)
        else:
            raise TypeError("Direction must be Direction type.")

    def connect_serial(self, discover_port=True):
        """Connects to Bittle.

        Parameters:
            discover_port (bool): If True, connects to the first
            communication port associated to CH340, otherwise connects to
            serialManager.port.

        Returns:
            res (bool) : True if connected, False otherwise.
        """
        if isinstance(discover_port, bool):
            pass
        else:
            raise TypeError("Value type must be bool.")
        res = False
        if discover_port:
            port_found = self.serialManager.discover_port()
        self.serialManager.initialize()
        res = self.serialManager.connect()
        return res

    def send_command_serial(self, command):
        """Sends command to Bittle through serial connection.

        Parameters:
            command (Comand) : Command to send.
        """
        if isinstance(command, Command):
            self.serialManager.send_msg(self._commands[command])
        else:
            raise TypeError("Command type must be Command.")

    def send_msg_serial(self, message):
        """Sends custom message to Bittle through serial connection.

        Parameters:
            message (str) : Message to send.
        """
        if isinstance(message, str):
            self.serialManager.send_msg(message)
        else:
            raise TypeError("Message type must be str.")

    def receive_msg_serial(self):
        """Receives a message from Bittle through serial connection.

        Returns:
            data (bytes) : Received data.
        """
        return self.serialManager.recv_msg()

    def send_movement_serial(self, direction):
        """Sends movement commands with current gait through serial
        connection.
        """
        if isinstance(direction, Direction):
            command = ''
            if direction in [Direction.BACKWARD, Direction.BACKWARDLEFT,
                             Direction.BACKWARDRIGHT]:
                command = 'kbk' + direction[1:]
            else:
                command = self.gait.value + direction.value
            self.send_msg_serial(command)
        else:
            raise TypeError("Direction must be Direction type.")

    def disconnect_serial(self):
        """Closes Serial connection.
        """
        self.serialManager.close_connection()