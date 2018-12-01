from cozypy.constant import DeviceType, DeviceState
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
        if self.client:
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
    pass

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
        return self.get_state(DeviceState.ECO_TEMPERATURE_STATE)

    @property
    def operation_mode(self):
        return self.get_state(DeviceState.OPERATING_MODE_STATE)

    @property
    def operation_list(self):
        return self.get_state_definition(DeviceState.OPERATING_MODE_STATE)


class CozytouchPlace(CozytouchObject):

    def __init__(self, data):
        super(CozytouchPlace, self).__init__(data)

