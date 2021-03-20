"""Connect to Bittle, control and manage its behaviour.

bittleManager is a high level module that allows connecting to Bittle through
Bluetooth or WiFi, define Bittle's behaviour and send/receive commands to
control it.
"""

import uuid

from enum import Enum

from .bluetoothManager import *

__author__ = "EnriqueMoran"

__version__ = "v0.1"


class Gait(Enum):
    """Defines avaliable gaits.
    """
    WALK = 1
    CRAWL = 2
    TROT = 3
    RUN = 4


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


COMMANDS = {  # Command : message to Bittle
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
    Command.ZERO: 'kzero'
}


class Bittle:
    """High level class that represents your Bittle.

    Attributes
    ----------
    id : uuid.UUID
        Bittle's unique id.
    bluetoothManager : BluetoothManager
        Manager for sending message to Bittle through Bluetooth connection.
    wifiManager : WifiManager
        Manager for sending message to Bittle through WiFi connection.
    serialManager : SerialManager
        Manager for sending message to Bittle through Serial connection.
    gait : Gait
        Current gait.

    Methods
    -------
    connectBluetooth(get_first_bittle):
        Connects to Bittle through Bluetooth connection.
    sendCommandBluetooth(command):
        Sends a command to Bittle through Bluetooth connection.
    sendMsgBluetooth(message):
        Sends a custom message to Bittle through Bluetooth connection.
    receiveMsgBluetooth(buffer_size):
        Returns received message from Bittle through Bluetooth connection.
    disconnectBluetooth():
        Closes Bluetooth connection with Bittle.
    """

    def __init__(self):
        self._id = uuid.uuid4()  # Bittle's id
        self.bluetoothManager = BluetoothManager()
        self.wifiManager = None
        self.serialManager = None
        self.gait = Gait.WALK  # Current gait

    def __eq__(self, other):
        return self._id == other._id

    def __str__(self):  # TODO: Complete
        return f"Bittle with id '{self._id}' Bluetooth name: " \
                f"'{self.bluetoothManager.name} ' MAC address: " \
                f"'{self.bluetoothManager.address}'"

    def connectBluetooth(self, get_first_bittle=True):
        """Connects to Bittle.

        Parameters:
            get_first_bittle (bool): If True, connects to the first
            "BittleSPP" found device, otherwise connects to
            bluetoothManager.name device.

        Returns:
            res (bool) : True if connected, False otherwise.
        """
        res = False
        name, addr = self.bluetoothManager.initialize_name_address_port(
                     get_first_bittle)
        if name and addr:  # Bittle found among avaliable paired devices
            res = self.bluetoothManager.connect()
        return res

    def sendCommandBluetooth(self, command):
        """Sends command to Bittle through Bluetooth connection.

        Parameters:
            command (Comand) : Command to send.
        """
        if isinstance(command, Command):
            self.bluetoothManager.sendMsg(COMMANDS[command])
        else:
            raise TypeError("Command type must be Command.")

    def sendMsgBluetooth(self, message):
        """Sends custom message to Bittle through Bluetooth connection.

        Parameters:
            message (str) : Message to send.
        """
        if isinstance(message, str):
            self.bluetoothManager.sendMsg(message)
        else:
            raise TypeError("Message type must be str.")

    def receiveMsgBluetooth(self, buffer_size=1024):
        """Receives a message from Bittle through Bluetooth connection.

        Parameters:
            buffer_size (int) : Buffer size.

        Returns:
            data (bytes) : Received data.
        """
        return self.bluetoothManager.recvMsg(buffer_size)

    def disconnectBluetooth(self):
        """Closes Bluetooth connection.
        """
        self.bluetoothManager.closeConnection()
