import time

from cozypy.constant import DeviceType, DeviceState, DeviceCommand
from cozypy.exception import CozytouchException


class CozytouchObject:

    def __init__(self, data:dict):
        self.client = None
        self.data = data

    @property
    def id(self):
        return self.data["oid"]

    @property
    def name(self):
        return self.data["label"]

    @property
    def creationTime(self):
        return self.data["creationTime"]

    @property
    def lastUpdateTime(self):
        return self.data["lastUpdateTime"]


class CozytouchDevice(CozytouchObject):

    def __init__(self, data:dict):
        super(CozytouchDevice, self).__init__(data)
        self.states = data["states"]
        self.place = None

    @property
    def deviceUrl(self):
        return self.data["deviceURL"]

    @property
    def widget(self):
        return DeviceType(self.data['widget'])

    def get_state_definition(self, state:DeviceState):
        for definition in self.data["definition"]["states"]:
            if definition["qualifiedName"] == state.value:
                return definition
        return None

    def get_state(self, state:DeviceState, value_only=True):
        for s in self.states:
            if s["name"] == state.value:
                return s["value"] if value_only else s
        return None

    def has_state(self, state:DeviceState):
        for s in self.states:
            if s["name"] == state.value:
                return True
        return False

    def update(self):
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        updated_data = self.client.get_states([self])
        self.states = updated_data["devices"][0]["states"]

    @staticmethod
    def build(data, client, place):
        device = None
        if data["widget"] == DeviceType.OCCUPANCY.value:
            device = CozytouchOccupancySensor(data)
        elif data["widget"] == DeviceType.TEMPERATURE.value:
            device = CozytouchTemperatureSensor(data)
        elif data["widget"] == DeviceType.ELECTRECITY.value:
            device = CozytouchElectricitySensor(data)
        elif data["widget"] == DeviceType.CONTACT.value:
            device = CozytouchContactSensor(data)

        if device is None:
            raise CozytouchException("Unknown device %s" % data["widget"])

        device.client = client
        device.place = place
        return device

class CozytouchContactSensor(CozytouchDevice):
    pass


class CozytouchElectricitySensor(CozytouchDevice):

    @property
    def consumption(self):
        return self.get_state(DeviceState.ELECTRIC_ENERGY_CONSUMTION_STATE)


class CozytouchTemperatureSensor(CozytouchDevice):

    @property
    def temperature(self):
        return self.get_state(DeviceState.TEMPERATURE_STATE)


class CozytouchOccupancySensor(CozytouchDevice):

    @property
    def is_occupied(self):
        state = self.get_state(DeviceState.OCCUPANCY_STATE)
        if state == "noPersonInside":
            return False
        elif state == "PersonInside":
            return True
        return False


class CozytouchHeater(CozytouchDevice):

    def __init__(self, data:dict):
        super(CozytouchHeater, self).__init__(data)
        self.sensors = []

    def __get_sensors(self, type:DeviceType):
        for sensor in self.sensors:
            if sensor.widget == type:
                return sensor
        return None

    @property
    def is_on(self):
        return self.get_state(DeviceState.ON_OFF_STATE)

    @property
    def is_away(self):
        away = self.get_state(DeviceState.AWAY_STATE)
        if away is None:
            return False
        return True if away == "on" else False

    @property
    def temperature(self):
        sensor = self.__get_sensors(DeviceType.TEMPERATURE)
        if sensor is None:
            return 0
        return sensor.temperature

    @property
    def comfort_temperature(self):
        return self.get_state(DeviceState.COMFORT_TEMPERATURE_STATE)

    @property
    def eco_temperature(self):
        comfort_temp = self.comfort_temperature
        if comfort_temp is None:
            return 0
        return comfort_temp - self.get_state(DeviceState.ECO_TEMPERATURE_STATE)

    @property
    def operation_mode(self):
        return self.get_state(DeviceState.OPERATING_MODE_STATE)

    @property
    def operation_list(self):
        definition = self.get_state_definition(DeviceState.OPERATING_MODE_STATE)
        if definition is not None:
            return definition["values"]
        return []

    @property
    def supported_states(self):
        supported_state = [state for state in DeviceState if self.has_state(state)]
        for state in DeviceState:
            if state in supported_state:
                continue
            for sensor in self.sensors:
                if sensor.has_state(state):
                    supported_state.append(state)
                    break
        return supported_state

    def is_state_supported(self, state:DeviceState):
        return state in self.supported_states

    def set_operation_mode(self, mode):
        if not  self.has_state(DeviceState.OPERATING_MODE_STATE):
            raise CozytouchException("Unsupported command %s" % DeviceCommand.SET_OPERATION_MODE)
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        self.client.send_command("Change operation mode", self, DeviceCommand.SET_OPERATION_MODE, [mode])

    def set_eco_temperature(self, temperature):
        if not  self.has_state(DeviceState.ECO_TEMPERATURE_STATE):
            raise CozytouchException("Unsupported command %s" % DeviceCommand.SET_ECO_TEMP)
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        temp = self.comfort_temperature - temperature
        self.client.send_command("Change eco temperature", self, DeviceCommand.SET_ECO_TEMP, [temp])

    def set_comfort_temperature(self, temperature):
        if not  self.has_state(DeviceState.COMFORT_TEMPERATURE_STATE):
            raise CozytouchException("Unsupported command %s" % DeviceCommand.SET_COMFORT_TEMP)
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        self.client.send_command("Change comfort temperature", self, DeviceCommand.SET_COMFORT_TEMP, [temperature])

    def turn_away_mode_off(self):
        if not  self.has_state(DeviceState.AWAY_STATE):
            raise CozytouchException("Unsupported command %s" % DeviceCommand.SET_AWAY_MODE)
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        self.client.send_command("Change away mode", self, DeviceCommand.SET_AWAY_MODE, ["off"])

    def turn_away_mode_on(self):
        if not  self.has_state(DeviceState.AWAY_STATE):
            raise CozytouchException("Unsupported command %s" % DeviceCommand.SET_AWAY_MODE)
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        self.client.send_command("Change away mode", self, DeviceCommand.SET_AWAY_MODE, ["on"])

    def update(self):
        if self.client is None:
            raise CozytouchException("Unable to update heater")
        time.sleep(2)
        for sensor in self.sensors:
            sensor.update()
        super(CozytouchHeater, self).update()

class CozytouchPlace(CozytouchObject):

    def __init__(self, data):
        super(CozytouchPlace, self).__init__(data)

