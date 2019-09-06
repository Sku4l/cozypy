from cozypy.constant import DeviceType
from cozypy.exception import CozytouchException
from cozypy.objects import CozytouchDevice, CozytouchPlace


class SetupHandler:

    def __init__(self, data, client):
        self.client = client
        self.data = data
        self.places = []
        self.heaters = []

        self.__build_places(data["rootPlace"])
        self.__build_devices(data["devices"])

    def __build_places(self, place):
        for subPlace in place["subPlaces"]:
            self.__build_places(subPlace)
        self.places.append(CozytouchPlace(place))

    def __build_devices(self, devices):
        sensors = []
        heaters = []
        for device in devices:
            device_class = DeviceType.from_str(device["widget"])
            if device_class in [DeviceType.HEATER, DeviceType.HEATER_PASV]:
                heaters.append(device)
            else:
                sensors.append(device)

        def extract_id(url):
            if '#' not in url:
                return url
            return url[0:url.index("#")]

        for heater in heaters:
            place: CozytouchPlace = self.__find_place(heater["placeOID"])
            if place is None:
                raise CozytouchException("Place {name} not found".format(name=heater["placeOID"]))
            heater_url = extract_id(heater["deviceURL"])
            heater_sensors = [CozytouchDevice.build(sensor, self.client, place) for sensor in sensors if extract_id(sensor["deviceURL"]) == heater_url]
            heater = CozytouchDevice.build(heater, self.client, place, sensors=heater_sensors)
            self.heaters.append(heater)

    def __find_place(self, oid):
        for place in self.places:
            if place.id == oid:
                return place
        return None


class DevicesHandler:

    def __init__(self, data, client):
        self.client = client
        self.data = data
        self.devices = []
        self.__build_devices(data)

    def __build_devices(self, data):
        for device in data:
            self.devices.append(CozytouchDevice.build(device, self))
