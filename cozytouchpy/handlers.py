import logging
from .constant import DeviceType
from .exception import CozytouchException
from .objects import CozytouchDevice, CozytouchPlace, CozytouchGateway, DeviceMetadata

logger = logging.getLogger(__name__)


class SetupHandler:

    def __init__(self, data, client):
        self.client = client
        self.data = data
        self.pods = []
        self.places = []
        self.heaters = []
        self.sensors = []
        self.water_heaters = []
        self.__build_places(data["rootPlace"])
        self.__build_gateways(data["gateways"])
        self.__build_devices(data["devices"])

    def __build_places(self, place):
        for subPlace in place["subPlaces"]:
            self.__build_places(subPlace)
        self.places.append(CozytouchPlace(place))

    def __build_gateways(self, gateways):
        self.gateways = []
        for gateway in gateways:
            place = self.__find_place(gateway)
            self.gateways.append(CozytouchGateway(gateway, place))

    def __build_devices(self, devices):
        sensors = []

        for idx in range(len(devices) - 1, -1, -1):
            device_type = DeviceType.from_str(devices[idx]["widget"])
            if device_type not in DeviceType.sensors():
                continue
            sensors.append(devices[idx])
            del devices[idx]

        for device in devices:
            device_type = DeviceType.from_str(device["widget"])
            metadata = self.__parse_url(device["deviceURL"])
            gateway = self.__find_gateway(metadata.gateway_id)
            place = self.__find_place(device)
            cozyouch_device = CozytouchDevice.build(
                data=device,
                client=self.client,
                metadata=metadata,
                gateway=gateway,
                place=place
            )
            device_sensors = self.__link_sensors(sensors, place, gateway, cozyouch_device)
            cozyouch_device.sensors = device_sensors

            if device_type == DeviceType.POD:
                self.pods.append(cozyouch_device)
            elif device_type in [DeviceType.HEATER, DeviceType.PILOT_WIRE_INTERFACE]:
                self.heaters.append(cozyouch_device)
            elif device_type == DeviceType.WATER_HEATER:
                self.water_heaters.append(cozyouch_device)

    def __parse_url(self, url):
        scheme = url[0:url.find('://')]
        if scheme not in ["io", "internal"]:
            raise CozytouchException("Invalid url {url}".format(url=url))
        metadata = DeviceMetadata()
        metadata.scheme = scheme
        parts = url.replace(scheme + "://", "").replace("#", "/").split("/")
        parts_len = len(parts)
        if parts_len < 2:
            raise CozytouchException("Invalid url {url}".format(url=url))
        metadata.gateway_id = parts[0]
        metadata.device_id = parts[1]
        if parts_len == 3:
            metadata.entity_id = parts[2]
        return metadata

    def __extract_gateway(self, url):
        if '#' not in url:
            return url
        return url[0:url.index("#")]

    def __link_sensors(self, sensors, place:CozytouchPlace, gateway:CozytouchGateway, parent:CozytouchDevice):
        device_sensors = []
        for sensor in sensors:
            metadata = self.__parse_url(sensor["deviceURL"])
            if metadata.device_id == parent.metadata.device_id:
                device_sensors.append(
                    CozytouchDevice.build(
                        data=sensor,
                        client=self.client,
                        metadata=metadata,
                        gateway=gateway,
                        place=place,
                        parent=parent
                    )
                )
        self.sensors += device_sensors
        return device_sensors

    def __find_place(self, device):
        for place in self.places:
            if place.id == device["placeOID"]:
                return place
        raise CozytouchException(
            "Place {name} not found".format(name=device["placeOID"])
        )

    def __find_gateway(self, gateway_id):
        for gateway in self.gateways:
            if gateway.id == gateway_id:
                return gateway
        raise CozytouchException(
            "Gateway {id} not found".format(id=gateway_id)
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
