"""This module manages WiFi connection.

WifiManager allows sending commands to Bittle by using the ESP8266 REST API.
"""

import ipaddress
import requests


__author__ = "EnriqueMoran"


class WifiManager:
    """Main class to manage WiFi connection.

    Attributes
    ----------
    ip : str
        Bittle's ip address.
    http_address : str
        Bittle's REST API address.

    Methods
    -------
    get_status_code():
        Returns REST API actionpage request response code.
    has_connection():
        Returns True if there is connection to REST API, False otherwise.
    send_msg(msg):
        Sends a message to Bittle.
    """

    def __init__(self):
        self._ip = ""
        self._http_address = f""

    def __repr__(self):
        return f"WifiManager - ip: {self.ip}, " \
               f"http_address: {self.http_address}"

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, new_ip):
        if isinstance(new_ip, str) and new_ip:
            try:
                ipaddress.ip_address(new_ip)
            except:
                raise TypeError("Invalid IPv4 address.")
            self._ip = new_ip
            self._http_address = f"http://{new_ip}/"
        else:
            raise TypeError("IP must be non empty str.")

    @property
    def http_address(self):
        return self._http_address

    def get_status_code(self):
        """Returns Action Page request response.

        Returns:
            res (int) : Action Page request response code, -1 if
            there is no connection.
        """
        res = -1
        http_address = self.http_address + "actionpage"
        try:
            response = requests.get(http_address)
            res = response.status_code
        except:
            pass
        return res

    def has_connection(self):
        """Returns True if Action Page request response is 200, False
        otherwise.

        Returns:
            res (bool) : True if there is connection with REST API,
            False otherwise.
        """
        res = False
        http_address = self.http_address + "actionpage"
        try:
            response = requests.get(http_address)
            if response.status_code == 200:
                res = True
        except:
            pass
        return res

    def send_msg(self, msg):
        """Sends a message to Bittle. Returns request response (int).

        Parameters:
            msg (str) : Message to send.

        Returns:
            status_code (int) : Request response code, -1 if there is no
            connection with REST API.
        """
        res = -1
        if isinstance(msg, str) and msg:
            query = {'name': msg}
            http_address = self.http_address + "action"
            try:
                response = requests.get(http_address, params=query)
                res = response.status_code
            except:
                pass
            return res
        else:
            raise TypeError("Message must be non empty str.")
