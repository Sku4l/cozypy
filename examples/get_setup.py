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

    print()
    for heater in setup.heaters:
        print("\t", heater.name)
        print("\t\t", heater.id)
        print("\t\t", heater.place.name)
        print("\t\t", heater.supported_states)
        print("\t\t", heater.is_on)
        print("\t\t", heater.operating_mode)
        for state in heater.supported_states:
            print("\t\t", state.value, heater.get_state(state))

        if heater.id == "7b56551a-badd-4dae-b12a-7a5864d8e6b5":
            heater.set_targeting_heating_level("comfort")
            heater.update()
        if len(heater.sensors) > 0:
            print("\t\tSensors")
            for sensor in heater.sensors:
                print("\t\t\t {id} {name} {type}".format(id=sensor.id, name=sensor.name, type=sensor.widget))
                for sensor_state in sensor.states:
                    print("\t\t\t\t {name}: {value}".format(name=sensor_state["name"], value=sensor_state["value"]))



except CozytouchException as e:
    logger.exception(e)