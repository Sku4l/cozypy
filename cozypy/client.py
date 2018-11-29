import json

import requests

from cozypy.constant import USER_AGENT, COZYTOUCH_ENDPOINT
from cozypy.exception import CozytouchException
from cozypy.handlers import SetupHandler


class CozytouchClient:

    def __init__(self, userId, userPassword):
        self.session = requests.Session()
        self.userId = userId
        self.userPassword = userPassword
        self.__authenticate()

    def __authenticate(self):
        """ Authenticate using userId and userPassword """

        headers = {'User-Agent': USER_AGENT}
        payload = {'userId': self.userId,'userPassword': self.userPassword}
        response = self.session.post(COZYTOUCH_ENDPOINT + "login",headers=headers,data=payload)

        if response.status_code != 200:
            raise CozytouchException("Authentication failed")

    def get_setup(self):
        """ Get cozytouch setup (devices, places) """

        headers = {'User-Agent': USER_AGENT}
        response = self.session.get(COZYTOUCH_ENDPOINT + '/getSetup', headers=headers)

        if response.status_code != 200:
            raise CozytouchException("Unable to retrieve setup %s " % response.content)

        return SetupHandler(response)

    def get_states(self, devices: list):
        """ Get devices states """
        headers = {'User-Agent': USER_AGENT, 'Content-type': 'application/json'}
        payload = [
            {
             "deviceURL": device.deviceUrl,
             "states":[{'name': state["name"]} for state in device.states]
            }
            for device in devices
        ]
        response = self.session.post(COZYTOUCH_ENDPOINT + '/getStates', headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise CozytouchException("Unable to retrieve devices states %s" % response.content)

        return response.json()

    def send_command(self, device, commands):
        """ Get devices states """
        headers = {'User-Agent': USER_AGENT, 'Content-type': 'application/json'}
        payload = [
            {
             "deviceURL": device.deviceUrl,
             "commands": commands
            }
        ]
        response = self.session.post(COZYTOUCH_ENDPOINT + '/apply', headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise CozytouchException("Unable to send command %s" % response.content)

        return response.json()