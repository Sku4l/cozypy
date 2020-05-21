"""Describe objects for cozytouch."""
import logging

from ..constant import DeviceState, DeviceType
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
        return DeviceType(self.data["widget"])

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
        return self.place.name + " " + self.widget.name.replace("_", " ").capitalize()

    @property
    def version(self):
        """Version."""
        return self.get_state(DeviceState.VERSION_STATE)

    def get_state_definition(self, state: DeviceState):
        """Get definition."""
        for definition in self.data["definition"]["states"]:
            if definition["qualifiedName"] == state.value:
                return definition
        return None

    def get_state(self, state: DeviceState, value_only=True):
        """Get state."""
        for s in self.states:
            if s["name"] == state.value:
                return s["value"] if value_only else s
        return None

    def set_state(self, state: DeviceState, value):
        """Set state."""
        for s in self.states:
            if s["name"] == state.value:
                s["value"] = value
                break

    def get_values_definition(self, attribut: str, state: DeviceState):
        """Get all values for a definiion."""
        definition = self.get_state_definition(state)
        if definition is None:
            return []
        return [attribut.from_str(value) for value in definition["values"]]

    def has_state(self, state: DeviceState):
        """State."""
        for s in self.states:
            if s["name"] == state.value:
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
            widget=self.widget.name.capitalize(),
            name=self.name,
            model=self.model,
            manufacturer=self.manufacturer,
            version=self.version,
        )
