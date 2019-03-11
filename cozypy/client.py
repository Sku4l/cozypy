import json

import requests

from cozypy.constant import USER_AGENT, COZYTOUCH_ENDPOINT, DeviceCommand
from cozypy.exception import CozytouchException
from cozypy.handlers import SetupHandler


class CozytouchClient:

    def __init__(self, username, password, timeout=60, max_retry=3):
        self.session = requests.Session()
        self.retry = 0
        self.max_retry = max_retry
        self.username = username
        self.password = password
        self.timeout = timeout
        self.__authenticate()

    def __authenticate(self):
        """ Authenticate using username and userPassword """

        headers = {'User-Agent': USER_AGENT}
        payload = {'userId': self.username,'userPassword': self.password}
        response = self.session.post(
            COZYTOUCH_ENDPOINT + "login",
            headers=headers,
            data=payload,
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise CozytouchException("Authentication failed")

    def __retry(self, response, callback, *kwargs):
        if response.status_code == 401 and self.retry < self.max_retry:
            self.retry += 1
            self.__authenticate()
            callback(kwargs)
        else:
            self.retry = 0

    def get_setup(self, *args):
        """ Get cozytouch setup (devices, places) """

        headers = {'User-Agent': USER_AGENT}
        response = self.session.get(
            COZYTOUCH_ENDPOINT + '/getSetup',
            headers=headers,
            timeout=self.timeout
        )

        self.__retry(response, self.get_setup)

        if response.status_code != 200:
            raise CozytouchException("Unable to retrieve setup %s " % response.content)

        return SetupHandler(response.json(), self)

    def get_states(self, devices: list, *args):
        """ Get devices states """
        headers = {'User-Agent': USER_AGENT, 'Content-type': 'application/json'}
        payload = [
            {
             "deviceURL": device.deviceUrl,
             "states":[{'name': state["name"]} for state in device.states]
            }
            for device in devices
        ]
        response = self.session.post(
            COZYTOUCH_ENDPOINT + '/getStates',
            headers=headers,
            data=json.dumps(payload),
            timeout=self.timeout
        )

        self.__retry(response, self.get_states, *args)

        if response.status_code != 200:
            raise CozytouchException("Unable to retrieve devices states %s" % response.content)

        return response.json()

    def send_command(self, label, device, command:DeviceCommand, parameters = None, *args):
        """ Get devices states """
        headers = {'User-Agent': USER_AGENT, 'Content-type': 'application/json'}
        payload = {
            "label": label,
            "actions": [
                {
                 "deviceURL": device.deviceUrl,
                 "commands": [
                     {"name": command.value, "parameters": parameters}
                 ]
                }
            ]
        }
        response = self.session.post(
            COZYTOUCH_ENDPOINT + '/apply',
            headers=headers,
            data=json.dumps(payload),
            timeout=self.timeout
        )

        self.__retry(response, self.send_command, *args)

        if response.status_code != 200:
            raise CozytouchException("Unable to send command %s" % response.content)

        json_response = response.json()
        print(json_response)
        return json_response