"""Construct class cozytouch."""

import logging
from .constant import DeviceType
from .exception import CozytouchException
from .utils import DeviceMetadata
from .objects import (
    CozytouchDevice,
    CozytouchPlace,
    CozytouchGateway,
    CozytouchHeater,
    CozytouchHeatPump,
    CozytouchPod,
    CozytouchWaterHeater,
    CozytouchBoiler,
    CozytouchContactSensor,
    CozytouchCumulativeFossilEnergyConsumptionSensor,
    CozytouchElectrecitySensor,
    CozytouchOccupancySensor,
    CozytouchTemperatureSensor,
)

logger = logging.getLogger(__name__)


class SetupHandler:
    """Set handler."""

    def __init__(self, data, client):
        """Initialize handler."""
        self.client = client
        self.data = data
        self.pods = []
        self.places = []
        self.heaters = []
        self.sensors = []
        self.water_heaters = []
        self.boilers = []
        self.heat_pumps = []
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
            device_type = devices[idx]["widget"]
            if device_type not in DeviceType.sensors():
                continue
            sensors.append(devices[idx])
            del devices[idx]

        for device in devices:
            try:
                device_type = device["widget"]
                metadata = self.parse_url(device["deviceURL"])
                gateway = self.__find_gateway(metadata.gateway_id)
                place = self.__find_place(device)
                cozyouch_device = DevicesHandler.build(
                    data=device,
                    client=self.client,
                    metadata=metadata,
                    gateway=gateway,
                    place=place,
                )
                device_sensors = self.__link_sensors(
                    sensors, place, gateway, cozyouch_device
                )
                cozyouch_device.sensors = device_sensors
                if device_type == DeviceType.POD:
                    self.pods.append(cozyouch_device)
                elif device_type in [
                    DeviceType.HEATER,
                    DeviceType.PILOT_WIRE_INTERFACE,
                    DeviceType.APC_HEATING_ZONE,
                ]:
                    self.heaters.append(cozyouch_device)
                elif device_type in [DeviceType.APC_HEAT_PUMP]:
                    self.heat_pumps.append(cozyouch_device)
                elif device_type in [
                    DeviceType.APC_BOILER,
                ]:
                    self.boilers.append(cozyouch_device)
                elif device_type in [
                    DeviceType.WATER_HEATER,
                    DeviceType.APC_WATER_HEATER,
                ]:
                    self.water_heaters.append(cozyouch_device)
            except CozytouchException as e:
                logger.warning("Error building device, skipping: %s", e)

    @staticmethod
    def parse_url(url):
        """Parse url."""
        scheme = url[0 : url.find("://")]
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

    def __link_sensors(
        self,
        sensors,
        place: CozytouchPlace,
        gateway: CozytouchGateway,
        parent: CozytouchDevice,
    ):
        device_sensors = []
        for sensor in sensors:
            metadata = self.parse_url(sensor["deviceURL"])
            if metadata.device_id == parent.metadata.device_id:
                device_sensors.append(
                    DevicesHandler.build(
                        data=sensor,
                        client=self.client,
                        metadata=metadata,
                        gateway=gateway,
                        place=place,
                        parent=parent,
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
        raise CozytouchException("Gateway {id} not found".format(id=gateway_id))


class DevicesHandler:
    """Devices."""

    def __init__(self, data, client):
        """Initialize."""
        self.client = client
        self.data = data
        self.devices = []
        self.__build_devices(data)

    def __build_devices(self, data):
        for device in data:
            try:
                self.devices.append(self.build(device, self))
            except CozytouchException as e:
                logger.warning("Error building device, skipping: %s", e)

    @staticmethod
    def build(
        data, client, metadata=None, gateway=None, place=None, sensors=None, parent=None
    ):
        """Build device object."""
        if sensors is None:
            sensors = []
        device = None
        if "widget" not in data or "uiClass" not in data:
            raise CozytouchException("Unable to identify device")
        device_class = data["widget"] if "widget" in data else data["uiClass"]
        if device_class == DeviceType.OCCUPANCY:
            device = CozytouchOccupancySensor(data)
        elif device_class == DeviceType.POD:
            device = CozytouchPod(data)
        elif device_class == DeviceType.TEMPERATURE:
            device = CozytouchTemperatureSensor(data)
        elif device_class == DeviceType.ELECTRECITY:
            device = CozytouchElectrecitySensor(data)
        elif device_class == DeviceType.CONTACT:
            device = CozytouchContactSensor(data)
        elif device_class == DeviceType.FOSSIL_ENERGY:
            device = CozytouchCumulativeFossilEnergyConsumptionSensor(data)
        elif device_class in [
            DeviceType.HEATER,
            DeviceType.PILOT_WIRE_INTERFACE,
            DeviceType.APC_HEATING_ZONE,
        ]:
            device = CozytouchHeater(data)
        elif device_class in [DeviceType.APC_BOILER]:
            device = CozytouchBoiler(data)
        elif device_class in [DeviceType.APC_HEAT_PUMP]:
            device = CozytouchHeatPump(data)
        elif device_class in [
            DeviceType.WATER_HEATER,
            DeviceType.APC_WATER_HEATER,
        ]:
            device = CozytouchWaterHeater(data)
        if device is None:
            raise CozytouchException("Unknown device {type}".format(type=device_class))

        device.client = client
        device.metadata = metadata
        device.gateway = gateway
        device.place = place
        device.parent = parent
        return device
