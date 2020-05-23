"""Describe objects for cozytouch."""
import logging

from ..constant import DeviceState
from ..exception import CozytouchException
from ..utils import DeviceMetadata
from .gateway import CozytouchGateway
from .object import CozytouchObject
from .place import CozytouchPlace

logger = logging.getLogger(__name__)


class CozytouchDevice(CozytouchObject):
    """Device."""

    def __init__(self, data: dict):
        """Initialize."""
        super(CozytouchDevice, self).__init__(data)
        self.states = data["states"]
        self.sensors = []
        self.metadata: DeviceMetadata = None
        self.gateway: CozytouchGateway = None
        self.place: CozytouchPlace = None
        self.parent: CozytouchDevice = None

    @property
    def deviceUrl(self):
        """Device url."""
        return self.metadata.base_url

    @property
    def widget(self):
        """Widget."""
        return self.data["widget"]

    @property
    def manufacturer(self):
        """Manufacturer."""
        return self.get_state(DeviceState.MANUFACTURER_NAME_STATE)

    @property
    def model(self):
        """Model."""
        return self.get_state(DeviceState.MODEL_STATE)

    @property
    def name(self):
        """Name."""
        return self.place.name + " " + self.widget.replace("_", " ").capitalize()

    @property
    def version(self):
        """Version."""
        return self.get_state(DeviceState.VERSION_STATE)

    def get_state(self, name):
        """Get state value."""
        for state in self.states:
            if state.get("name") == name:
                return state.get("value")

    def set_state(self, state, value):
        """Set state value."""
        for state_name in self.states:
            if state_name == state:
                state_name = value
                break

    def get_definition(self, definition):
        """Get definition value."""
        for state in self.data["definition"].get("states"):
            if state.get("qualifiedName") == definition:
                return state.get("values")

    def get_sensors(self, device_type):
        """Get sensor."""
        for sensor in self.sensors:
            if sensor.widget == device_type:
                return sensor
        return None

    def has_state(self, state):
        """Search name state."""
        for state_name in self.states.keys():
            if state_name == state:
                return True
        return False

    async def update(self):
        """Update device."""
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        logger.debug("Update states sensors")
        self.states = await self.client.get_device_info(self.deviceUrl)

    def __str__(self):
        """Definition."""
        return "{widget} (name={name}, model={model}, manufacturer={manufacturer}, version={version})".format(
            widget=self.widget.capitalize(),
            name=self.name,
            model=self.model,
            manufacturer=self.manufacturer,
            version=self.version,
        )
