"""Cozytouch API."""
import logging
import json
import re
import requests
import urllib.parse

from requests.exceptions import RequestException

from .constant import USER_AGENT, COZYTOUCH_ENDPOINTS
from .exception import CozytouchException, AuthentificationFailed, HttpRequestFailed
from .handlers import SetupHandler, DevicesHandler
from .utils import CozytouchEncoder

logger = logging.getLogger(__name__)


class CozytouchClient:
    """Client session."""

    def __init__(self, username, password, timeout=60, max_retry=3):
        """Initializate session."""
        self.session = requests.Session()
        self.retry = 0
        self.max_retry = max_retry
        self.username = username
        self.password = password
        self.timeout = timeout
        self.is_connected = False

    @classmethod
    def build_url(cls, resource, data):
        """Build url."""
        if resource not in COZYTOUCH_ENDPOINTS:
            raise CozytouchException(
                "Bad resource: {resource}".format(resource=resource)
            )
        url = COZYTOUCH_ENDPOINTS[resource]

        matches = re.findall("(?P<text>\\[(?P<param>[^] ]+)\\])", url)
        for text, key in matches:
            url = url.replace(text, urllib.parse.quote_plus(data[key]))

        return url

    def __make_request(
        self, resource, method="GET", data=None, headers=None, json_encode=True
    ):
        """Make call to Cozytouch API."""
        if not self.is_connected and resource != "login":
            raise AuthentificationFailed

        if data is None:
            data = {}
        logger.debug("Request: %s", data)
        if headers is None:
            headers = {}

        headers["User-Agent"] = USER_AGENT

        url = self.build_url(resource, data)
        if method == "GET":
            try:
                response = self.session.get(url, timeout=self.timeout)
            except RequestException as e:
                raise HttpRequestFailed("Error request", e)
        else:
            if json_encode:
                data = json.dumps(data, cls=CozytouchEncoder)
                headers["Content-Type"] = "application/json"

            try:
                response = self.session.post(
                    url, headers=headers, data=data, timeout=self.timeout
                )
            except RequestException as e:
                raise HttpRequestFailed("Error Request", e)
        logger.debug("Response: %s", response)
        return response

    def connect(self):
        """Authenticate using username and userPassword."""
        response = self.__make_request(
            "login",
            method="POST",
            data={"userId": self.username, "userPassword": self.password},
            json_encode=False,
        )
        logger.debug(response.cookies.get_dict())
        if response.status_code != 200:
            raise AuthentificationFailed(response.status_code)
        self.is_connected = True

    def __retry(self, response, callback, *args):
        if response.status_code == 401 and self.retry < self.max_retry:
            self.retry += 1
            self.connect()
            callback(*args)
        else:
            self.retry = 0

    def get_setup(self):
        """Get cozytouch setup (devices, places)."""
        response = self.__make_request("setup", method="GET")
        self.__retry(response, self.get_setup)

        if response.status_code != 200:
            response_json = response.json()
            raise CozytouchException(
                "Unable to retrieve setup: {error}[{code}]".format(
                    error=response_json["error"], code=response_json["errorCode"]
                )
            )
        return SetupHandler(response.json(), self)

    def get_devices(self):
        """.Get cozytouch setup (devices, places)."""
        response = self.__make_request("devices")
        self.__retry(response, self.get_devices)

        if response.status_code != 200:
            raise CozytouchException(
                "Unable to retrieve devices: {response}".format(
                    response=response.content
                )
            )

        return DevicesHandler(response.json(), self)

    def get_device_info(self, device_url):
        """Get cozytouch setup (devices, places)."""
        response = self.__make_request("deviceInfo", data={"device_url": device_url})
        self.__retry(response, self.get_devices, {"device_url": device_url})

        if response.status_code != 200:
            response_json = response.json()
            raise CozytouchException(
                "Unable to retrieve device {device_url}: {error}[{code}]".format(
                    device_url=device_url,
                    error=response_json["error"],
                    code=response_json["errorCode"],
                )
            )
        state = response.json()
        return state

    def get_device_state(self, device_url, state_name):
        """Get cozytouch setup (devices, places)."""
        response = self.__make_request(
            "stateInfo", data={"device_url": device_url, "state_name": state_name}
        )
        kwargs = {"device_url": device_url, "state_name": state_name}
        self.__retry(response, self.get_devices, kwargs)

        if response.status_code != 200:
            raise CozytouchException(
                "Unable to retrieve state {state_name} from device {device_url} : {response}".format(
                    device_url=device_url,
                    state_name=state_name,
                    response=response.content,
                )
            )

        return SetupHandler(response.json(), self)

    def send_commands(self, commands, *args):
        """Get devices states."""
        logger.debug("Request commands %s", str(commands))

        response = self.__make_request(
            "apply",
            method="POST",
            data=commands,
            headers={"Content-type": "application/json"},
        )
        self.__retry(response, self.send_commands, *args)

        if response.status_code != 200:
            response_json = response.json()
            raise CozytouchException(
                "Unable to send command : {error}[{code}]".format(
                    error=response_json["error"], code=response_json["errorCode"]
                )
            )

        logger.debug("Response commands %s", response.content)
        return response.json()
