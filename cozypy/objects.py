from cozypy.constant import DeviceType, DeviceState


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

    def get_state(self, state:DeviceState):
        for s in self.states:
            if s["name"] == state.value:
                return s["value"]
        return None


class CozytouchPlace(CozytouchObject):

    def __init__(self, data):
        super(CozytouchPlace, self).__init__(data)
        self.pods = []
        self.sensors = []
        self.heaters = []

    def add_device(self, device):
        if device.widget == DeviceType.HEATER:
            self.heaters.append(device)
        elif device.widget == DeviceType.POD:
            self.pods.append(device)
        else:
            self.sensors.append(device)

