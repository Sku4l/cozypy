"""Cozytouch API."""
import logging
import json
import re
import requests
import urllib.parse

from .constant import USER_AGENT, COZYTOUCH_ENDPOINTS
from .exception import CozytouchException
from .handlers import SetupHandler, DevicesHandler
from .utils import CozytouchEncoder

logger = logging.getLogger(__name__)


class CozytouchClient:
    """Client session."""

    def __init__(self, username, password, timeout=60, max_retry=3):
        """ Initialization."""
        self.session = requests.Session()
        self.retry = 0
        self.max_retry = max_retry
        self.username = username
        self.password = password
        self.timeout = timeout
        self.__authenticate()

    @classmethod
    def build_url(cls, resource, data):
        """ Build url"""
        if resource not in COZYTOUCH_ENDPOINTS:
            raise CozytouchException("Bad resource: {resource}".format(resource=resource))
        url = COZYTOUCH_ENDPOINTS[resource]

        matches = re.findall("(?P<text>\\[(?P<param>[^] ]+)\\])", url)
        for text, key in matches:
            url = url.replace(text, urllib.parse.quote_plus(data[key]))

        return url

    def __make_request(self, resource, method="GET", data=None, headers=None, json_encode=True):
        """ Make call to Cozytouch API"""
        if data is None:
            data = {}
        logger.debug("Request : {}".format(data))
        if headers is None:
            headers = {}

        headers["User-Agent"] = USER_AGENT

        url = self.build_url(resource, data)
        if method == "GET":
            response = self.session.get(url, timeout=self.timeout)
        else:
            if json_encode:
                data = json.dumps(data,  cls=CozytouchEncoder)
                headers["Content-Type"] = "application/json"

            response = self.session.post(
                url,
                headers=headers,
                data=data,
                timeout=self.timeout
            )

        return response

    def __authenticate(self):
        """ Authenticate using username and userPassword """
        response = self.__make_request(
            "login",
            method="POST",
            data={'userId': self.username, 'userPassword': self.password},
            json_encode=False
        )

        logger.debug(response.cookies.get_dict())
        if response.status_code != 200:
            raise CozytouchException("Authentication failed")

    def __retry(self, response, callback, *kwargs):
        if response.status_code == 401 and self.retry < self.max_retry:
            self.retry += 1
            self.__authenticate()
            callback(kwargs)
        else:
            self.retry = 0

    async def async_get_setup(self, *args):
        """ Get cozytouch setup (devices, places) """
        response = self.__make_request(
            "setup",
            method="GET"
        )
        self.__retry(response, self.async_get_setup)

        if response.status_code != 200:
            response_json = response.json()
            raise CozytouchException(
                "Unable to retrieve setup: {error}[{code}]".format(
                    error=response_json["error"], code=response_json["errorCode"]
                    )
            )

        return SetupHandler(response.json(), self)

    async def async_get_devices(self, *args):
        """ Get cozytouch setup (devices, places) """

        response = self.__make_request("devices")
        self.__retry(response, self.async_get_devices)

        if response.status_code != 200:
            raise CozytouchException("Unable to retrieve devices: {response}".format(
                response=response.content)
                )

        return DevicesHandler(response.json(), self)

    async def async_get_device_info(self, device_url, *args):
        """ Get cozytouch setup (devices, places) """

        response = self.__make_request("deviceInfo", data={"device_url": device_url})
        self.__retry(response, self.async_get_devices, {"device_url": device_url})

        if response.status_code != 200:
            response_json = response.json()
            raise CozytouchException(
                "Unable to retrieve device {device_url}: {error}[{code}]".format(
                    device_url=device_url, error=response_json["error"], code=response_json["errorCode"]
                    )
            )
        state = response.json()
        return state

    async def async_get_device_state(self, device_url, state_name, *args):
        """ Get cozytouch setup (devices, places) """

        response = self.__make_request("stateInfo", data={"device_url": device_url, "state_name": state_name})
        kwargs = {"device_url": device_url, "state_name": state_name}
        self.__retry(response, self.async_get_devices, kwargs)

        if response.status_code != 200:
            raise CozytouchException(
                "Unable to retrieve state {state_name} from device {device_url} : {response}".format(
                    device_url=device_url, state_name=state_name, response=response.content
                    )
            )

        return SetupHandler(response.json(), self)

    async def async_send_commands(self, commands, *args):
        """ Get devices states """

        logger.debug("Request commands {}".format(vars(commands)))
        response = self.__make_request(
            "apply",
            method="POST",
            data=commands,
            headers={'Content-type': 'application/json'}
        )
        self.__retry(response, self.async_send_commands, *args)

        if response.status_code != 200:
            response_json = response.json()
            raise CozytouchException(
                "Unable to send command : {error}[{code}]".format(
                    error=response_json["error"], code=response_json["errorCode"]
                    )
            )

        logger.debug("Response commands {}".format(response.content))
        return response.json()
