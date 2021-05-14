# pyBittle

pyBittle is an Open Source Python library for easily connecting to Bittle and controlling it.
This library provides a set of methods to communicating with Bittle through Bluetooth and WiFi, allowing to control it remotely.

In-depth documentation and usage examples: [pyBittle](https://enriquemoran95.gitbook.io/pybittle/).


## Usage example

Connecting to Bittle and sending commands is as easy as shown below:

```python
bittle = pyBittle.Bittle()  # This is your Bittle

is_connected = bittle.connect_bluetooth()  # Returns True if Bittle is connected to your computer

if is_connected:
    greet_command = pyBittle.Command.GREETING  # This is 'khi' message to be sent
    bittle.send_command_bluetooth(greet_command)  # Send 'khi' message through Bluetooth
    bittle.disconnect_bluetooth()
```

```python
bittle = pyBittle.Bittle()

bittle.wifiManager.ip = '192.168.1.241'  # This is your Bittle's IP address

push_up_command = pyBittle.Command.PUSHUP  # This is 'kpu' message to be sent

has_connection = bittle.has_wifi_connection()
if has_connection:
    bittle.send_command_wifi(push_up_command)  # Send 'kpu' message through WiFi
```

```python
bittle = pyBittle.Bittle()

is_connected = bittle.connect_serial()  # Returns True if Bittle is connected to your computer

if is_connected:
    stretch_command = pyBittle.Command.STRETCH  # This is 'kstr' message to be sent
    bittle.send_command_serial(stretch_command)  # Send 'kstr' message through Serial
    bittle.disconnect_serial()
```


## Installation

Install automatically using the following command:
```
pip install pyBittle
```

pyBittle has the following dependencies: [PyBluez](https://github.com/pybluez/pybluez) and [pySerial](https://github.com/pyserial/pyserial), install them manually using the following commands:

```
sudo apt-get install libbluetooth-dev
sudo apt-get install python-dev
pip install pybluez

pip install pyserial

git clone https://github.com/EnriqueMoran/pyBittle.git
pip install .
```