import numpy as np

from cozypy.exception import CozytouchException

from cozypy.constant import DeviceType, DeviceState, DeviceStateType


class CozytouchObject:

    def __init__(self, data:dict):
        self.oid = data["oid"]
        self.label = data["label"]
        self.creationTime = data["creationTime"]
        self.lastUpdateTime = data["lastUpdateTime"]


class CozytouchDevice(CozytouchObject):

    def __init__(self, data:dict):
        super(CozytouchDevice, self).__init__(data)
        self.states = data["states"]
        self.widget = DeviceType(data["widget"])

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


class CozytouchPlace(CozytouchObject):

    def __init__(self, data):
        super(CozytouchPlace, self).__init__(data)
        self.pods = []
        self.sensors = []
        self.heaters = []

    @property
    def temperature(self):
        return self.__aggregate_state(DeviceType.TEMPERATURE, DeviceState.CURRENT_TEMPERATURE_STATE)

    @property
    def on_off(self):
        return self.__aggregate_state(DeviceType.HEATER, DeviceState.ON_OFF_STATE)

    @property
    def comfort_temperature(self):
        return self.__aggregate_state(DeviceType.HEATER, DeviceState.COMFORT_TEMPERATURE_STATE)

    @property
    def eco_temperature(self):
        return self.comfort_temperature - self.__aggregate_state(DeviceType.HEATER, DeviceState.ECO_TEMPERATURE_STATE)

    def add_device(self, device):
        if device.widget == DeviceType.HEATER:
            self.heaters.append(device)
        elif device.widget == DeviceType.POD:
            self.pods.append(device)
        else:
            self.sensors.append(device)

    def __filter_devices(self, devices, state:DeviceState):
        return [device for device in devices if device.has_state(state)]

    def __aggregate_state(self, type:DeviceType, state:DeviceState):
        if type == DeviceType.HEATER:
            devices = self.__filter_devices(self.heaters, state)
        elif type == DeviceType.POD:
            devices = self.__filter_devices(self.pods, state)
        else:
            devices = self.__filter_devices(self.sensors, state)

        if devices is None or not len(devices):
            return None

        type = None
        values = []
        for device in devices:
            state_info = device.get_state(state, False)
            if state_info is not None:
                state_type = DeviceStateType(state_info["type"])
                if type is not None and type != state_type:
                    raise CozytouchException("Inconsistent state type")
                type = state_type
                if state_type in [DeviceStateType.INT, DeviceStateType.FLOAT, DeviceStateType.STR]:
                    values.append(state_info["value"])
                else:
                    raise CozytouchException("Unable to aggregate non numeric state")

        if not len(values):
            return None
        if type in [DeviceStateType.INT, DeviceStateType.FLOAT]:
            return np.average(values)
        elif type == DeviceStateType.STR:
            values, counts = np.unique(values, return_counts=True)
            idx = np.argmax(counts)
            value = values[idx]
            return value
        return None
