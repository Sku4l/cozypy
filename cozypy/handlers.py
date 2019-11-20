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
            if device_class == DeviceType.WATER_HEATER:
                water_heaters.append(device)
            else:
                sensors.append(device)

        for heater in heaters:
            place = self.__find_place(heater)
            heater_url = self.__extract_id(heater["deviceURL"])
            heater_sensors = self.__link_sensors(sensors, place, heater_url)
            heater = CozytouchDevice.build(heater, self.client, place, sensors=heater_sensors)
            self.heaters.append(heater)

        for water_heater in water_heaters:
            place = self.__find_place(water_heater)
            water_heater_url = self.__extract_id(water_heater["deviceURL"])
            wh_sensors = self.__link_sensors(sensors, place, water_heater_url)
            water_heater = CozytouchDevice.build(water_heater, self.client, place, sensors=wh_sensors)
            self.water_heaters.append(water_heater)

    def __extract_id(self, url):
        if '#' not in url:
            return url
        return url[0:url.index("#")]

    def __link_sensors(self, sensors, place, device_url):
        device_sensors = []
        for sensor in sensors:
            if self.__extract_id(sensor["deviceURL"]) == device_url:
                device_sensors.append(CozytouchDevice.build(sensor, self.client, place))
        return device_sensors

    def __find_place(self, device):
        for place in self.places:
            if place.id == device["placeOID"]:
                return place
        raise CozytouchException(
            "Place {name} not found".format(name=device["placeOID"])
        )


class DevicesHandler:

    def __init__(self, data, client):
        self.client = client
        self.data = data
        self.devices = []
        self.__build_devices(data)

    def __build_devices(self, data):
        for device in data:
            self.devices.append(CozytouchDevice.build(device, self))
