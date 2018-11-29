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
        print(place.label)
        if len(place.heaters) > 0:
            print("\tHeaters")
            for heater in place.heaters:
                print("\t\t %s" % heater.label)
        if len(place.sensors) > 0:
            print("\tSensors")
            for sensor in place.sensors:
                print("\t\t %s %s" % (sensor.label, sensor.widget))

        if len(place.pods) > 0:
            print("\tPods")
            for pod in place.pods:
                print("\t\t %s" % pod.label)

except CozytouchException as e:
    logger.exception(e)