class CozytouchSetup:

    def __init__(self, response):
        self.places = []
        self.devices = []
        self.__build_places(response["setup"]["rootPlace"])
        self.__build_devices(response["setup"]["devices"])


    def __build_places(self, place):
        for subPlace in place["subPlaces"]:
            self.__build_places(subPlace)
        self.places.append(CozytouchPlace(**place))

    def __build_devices(self, devices):
        for device in devices:
            dev = CozytouchDevice(
                oid=device["oid"],
                label=device["label"],
                creationTime=device["creationTime"],
                lastUpdateTime=device["lastUpdateTime"],
                deviceUrl=device["deviceURL"],
                widget=device["widget"],
                states=device["states"],
                place=self.__find_place(device["placeOID"])
            )
            self.devices.append(dev)

    def __find_place(self, oid):
        for place in self.places:
            if place.oid == oid:
                return place
        return None


class CozytouchDevice:

    def __init__(self, oid, label, creationTime, lastUpdateTime, deviceUrl, widget, states, place):
        self.oid = oid
        self.label = label
        self.creationTime = creationTime
        self.lastUpdateTime = lastUpdateTime
        self.deviceUrl = deviceUrl
        self.widget = widget
        self.states = states
        self.place = place

    def get_state(self, name):
        for state in self.states:
            if state["name"] == name:
                return state["value"]
        return None

class CozytouchPlace:

    def __init__(self, oid, label, creationTime, lastUpdateTime, **kwargs):
        self.oid = oid
        self.label = label
        self.creationTime = creationTime
        self.lastUpdateTime = lastUpdateTime
        self.devices = []
        self.kwargs = kwargs

    def add_device(self, device):
        self.devices.append(device)

