import os
import logging

from cozypy.client import CozytouchClient
from cozypy.exception import CozytouchException
from cozypy.objects import CozytouchHeater
from cozypy.constant import OperatingModeState

logger = logging.getLogger("cozytouch.examples")


clientId = os.environ['COZYTOUTCH_CLIENT_ID']
clientPassword = os.environ['COZYTOUTCH_CLIENT_PASSWORD']

try:
    client = CozytouchClient(clientId, clientPassword)
    devices = client.get_devices()
    states = client.get_device_info("io://0812-9894-4518/10071767#1")
    for state in states:
        print("\t\t", state["name"], state["value"])

    heater = CozytouchHeater({
        "deviceURL": "io://0812-9894-4518/10071767#1",
        "states": states
    })
    heater.client = client

    heater.set_eco_temperature(16)
    heater.set_comfort_temperature(18)
    heater.set_operating_mode(OperatingModeState.INTERNAL)
    heater.update()
    for state in heater.supported_states:
        print("\t\t", state.value, heater.get_state(state))

except CozytouchException as e:
    logger.exception(e)