from cozypy.constant import DeviceType
from cozypy.exception import CozytouchException
from cozypy.objects import CozytouchDevice, CozytouchPlace


class SetupHandler:

    def __init__(self, data, client):
        self.client = client
        self.data = data
        self.places = []
        self.heaters = []
        self.water_heaters = []
        self.__build_places(data["rootPlace"])
        self.__build_devices(data["devices"])

    def __build_places(self, place):
        for subPlace in place["subPlaces"]:
            self.__build_places(subPlace)
        self.places.append(CozytouchPlace(place))

    def __build_devices(self, devices):
        sensors = []
        heaters = []
        water_heaters = []
        for device in devices:
            device_class = DeviceType.from_str(device["widget"])
            if device_class in [DeviceType.HEATER, DeviceType.HEATER_PASV]:
                heaters.append(device)
            if device_class in [DeviceType.WATER_HEATER]:
                water_heaters.append(device)
            else:
                sensors.append(device)

        def extract_id(url):
            if '#' not in url:
                return url
            return url[0:url.index("#")]

        def link_sensors(sensors, place, device_url):
            device_sensors = []
            for sensor in sensors:
                if extract_id(sensor["deviceURL"]) == device_url:
                    device_sensors.append(CozytouchDevice.build(sensor, self.client, place))
            return device_sensors

        def find_place(device):
            place: CozytouchPlace = self.__find_place(device["placeOID"])
            if place is None:
                raise CozytouchException(
                    "Place {name} not found".format(name=device["placeOID"])
                )
            return place

        for heater in heaters:
            place = find_place(heater)
            heater_url = extract_id(heater["deviceURL"])
            heater_sensors = link_sensors(sensors, place, heater_url)
            heater = CozytouchDevice.build(heater, self.client, place, sensors=heater_sensors)
            self.heaters.append(heater)

        for water_heater in water_heaters:
            place = find_place(water_heater)
            water_heater_url = extract_id(water_heater["deviceURL"])
            wh_sensors = link_sensors(sensors, place, water_heater_url)
            water_heater = CozytouchDevice.build(water_heater, self.client, place, sensors=wh_sensors)
            self.water_heaters.append(water_heater)
    

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
