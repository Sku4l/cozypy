"""Describe objects for cozytouch."""
import logging

from ..constant import DeviceCommand as dc
from ..constant import DeviceState as ds
from ..constant import ModeState
from ..exception import CozytouchException
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchBoiler(CozytouchDevice):
    """Boiler."""

    @property
    def model(self):
        """Model."""
        return self.get_state(ds.PRODUCT_MODEL_NAME_STATE)

    @property
    def away_target_temperature(self):
        """Boost state."""
        return self.get_state(ds.ABSENCE_HEATING_TARGET_TEMPERATURE_STATE)

    @property
    def is_on(self):
        """Is alive."""
        return self.operating_mode != ModeState.STOP

    @property
    def current_temperature(self) -> float:
        """Return tempereture (middle water heater)."""

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""

    @property
    def is_away_mode_on(self) -> bool:
        """Return if away mode enabled."""

    @property
    def timeprogram_state(self):
        """Get all time program."""
        TimeProgram = {}
        for i in range(4):
            state = f"core:TimeProgram{i+1}State"
            TimeProgram.update({f"TimeProgram{i+1}": self.get_state(state)})
        return TimeProgram

    @property
    def operating_mode(self):
        """Return operation mode."""
        return self.get_state(ds.PASS_APC_OPERATING_MODE_STATE)

    @property
    def operating_mode_list(self):
        """Return operating mode list."""
        return self.get_definition(ds.PASS_APC_OPERATING_MODE_STATE)

    @property
    def supported_states(self) -> dict:
        """Supported states."""
        supported_states = [state["name"] for state in self.states]
        for sensor in self.sensors:
            sensor_states = [state["name"] for state in sensor.states]
            supported_states = list(set(supported_states + sensor_states))
        return supported_states

    def is_state_supported(self, state):
        """Return is supported ."""
        return state in self.supported_states

    async def set_operating_mode(self, mode):
        """Set operating mode."""
        mode_state = ds.PASS_APC_OPERATING_MODE_STATE
        actions = [
            (dc.SET_PASS_APC_OPERATING_MODE, mode),
            (dc.REFRESH_OPERATION_MODE, None),
        ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, mode)

    async def update(self):
        """Update boiler state."""
        if self.client is None:
            raise CozytouchException("Unable to update boiler")
        for sensor in self.sensors:
            logger.debug("Boiler: Update sensor")
            await sensor.update()
        await super(CozytouchBoiler, self).update()
