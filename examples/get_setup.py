import os
import logging

from cozypy.client import CozytouchClient
from cozypy.exception import CozytouchException


clientId = os.environ['COZYTOUCH_CLIENT_ID']
clientPassword = os.environ['COZYTOUCH_CLIENT_PASSWORD']

try:
    client = CozytouchClient(clientId, clientPassword)
    setup = client.get_setup()

    def print_device(device):
        print()
        print("\t Name:", device.name)
        print("\t\t Id:", device.id)
        print("\t\t Place:", device.place.name)
        print("\t\t Suported states:")
        for state in device.supported_states:
            print("\t\t\t", state)
        print("\t\t States value:")
        for state in device.supported_states:
            print("\t\t\t", state.value, device.get_state(state))
        print("\t\t Is on:", device.is_on)
        print("\t\t Operating mode:", device.operating_mode)
        if len(device.sensors) > 0:
            print("\t\t Sensors")
            for sensor in device.sensors:
                print("\t\t\t Id:", sensor.id)
                print("\t\t\t Name:", sensor.name)
                print("\t\t\t Type:", sensor.widget)
                for sensor_state in sensor.states:
                    print("\t\t\t\t {name}: {value}".format(name=sensor_state["name"], value=sensor_state["value"]))


    for place in setup.places:
        print(place.id)
        print(place.name)

    for water_heater in setup.water_heaters:
        print_device(water_heater)

    for heater in setup.heaters:
        print_device(heater)
        


except CozytouchException as e:
    logger.exception(e)