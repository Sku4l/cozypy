import os
import logging

from cozypy.client import CozytouchClient
from cozypy.exception import CozytouchException

logger = logging.getLogger("cozytouch.examples")


clientId = os.environ['COZYTOUTCH_CLIENT_ID']
clientPassword = os.environ['COZYTOUTCH_CLIENT_PASSWORD']

try:
    client = CozytouchClient(clientId, clientPassword)
    setup = client.get_setup()
    for place in setup.places:
        print(place.id)
        print(place.name)

    for heater in setup.heaters:
        print(heater.id)
        print(heater.name)

        if len(heater.sensors) > 0:
            print("\tSensors")
            for sensor in heater.sensors:
                print("\t\t %s %s %s" % (sensor.id, sensor.name, sensor.widget))


except CozytouchException as e:
    logger.exception(e)