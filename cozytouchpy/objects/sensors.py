"""Describe objects for cozytouch."""
import logging

from .device import CozytouchDevice
from ..constant import DeviceState

logger = logging.getLogger(__name__)


class CozytouchSensor(CozytouchDevice):
    """Generic sensor."""

    def __init__(self, data):
        """Initialize."""
        super(CozytouchSensor, self).__init__(data)
        delattr(self, "sensors")

    @property
    def id(self):
        """Return Unique id."""
        return self.parent.id + "_" + self.sensor_class

    @property
    def name(self):
        """Name."""
        name = self.parent.name if self.parent is not None else self.name
        return name + " " + self.sensor_class

    @property
    def sensor_class(self):
        """Class."""
        return "unknown"


class CozytouchContactSensor(CozytouchSensor):
    """Contact sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "contact"

    @property
    def is_opened(self):
        """State."""
        state = self.get_state(DeviceState.CONTACT_STATE)
        return state != "closed"


class CozytouchElectrecitySensor(CozytouchSensor):
    """Electrecity sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "consumption"

    @property
    def consumption(self):
        """State."""
        return int(self.get_state(DeviceState.ELECTRIC_ENERGY_CONSUMPTION_STATE))


class CozytouchTemperatureSensor(CozytouchSensor):
    """Temperature sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "temperature"

    @property
    def temperature(self):
        """State."""
        return self.get_state(DeviceState.TEMPERATURE_STATE)


class CozytouchOccupancySensor(CozytouchSensor):
    """Occupancy sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "occupancy"

    @property
    def is_occupied(self):
        """State."""
        return self.get_state(DeviceState.OCCUPANCY_STATE) == "personInside"


class CozytouchCumulativeFossilEnergyConsumptionSensor(CozytouchSensor):
    """Temperature sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "consumption"

    @property
    def temperature(self):
        """State."""
        return self.get_state(DeviceState.FOSSIL_ENERGY_CONSUMPTION_STATE)
