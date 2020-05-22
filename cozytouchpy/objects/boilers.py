"""Describe objects for cozytouch."""
import logging

from ..constant import (
    DeviceState,
    DeviceType,
    OperatingModeState,
)
from ..exception import CozytouchException
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchBoiler(CozytouchDevice):
    """Boiler."""

    def __init__(self, data: dict):
        """Initialize."""
        super(CozytouchBoiler, self).__init__(data)
        self.sensors = []

    def __get_sensors(self, device_type: DeviceType):
        for sensor in self.sensors:
            if sensor.widget == device_type:
                return sensor
        return None

    @property
    def model(self):
        """Model."""
        return self.get_state(DeviceState.PRODUCT_MODEL_NAME_STATE)

    @property
    def away_target_temperature(self):
        """Boost state."""
        return self.get_state(DeviceState.ABSENCE_HEATING_TARGET_TEMPERATURE_STATE)

    @property
    def is_on(self):
        """Is alive."""
        return self.operating_mode != OperatingModeState.STOP

    @property
    def timeprogram_state(self):
        """Get all time program."""
        TimeProgram = {}
        for i in range(4):
            state = DeviceState.from_str(f"core:TimeProgram{i+1}State")
            TimeProgram.update({f"TimeProgram{i+1}": self.get_state(state)})
        return TimeProgram

    @property
    def operating_mode(self):
        """Return operation mode."""
        return OperatingModeState.from_str(
            self.get_state(DeviceState.PASS_APC_OPERATING_MODE_STATE)
        )

    @property
    def operating_mode_list(self):
        """Return operating mode list."""
        return self.get_values_definition(
            OperatingModeState, DeviceState.PASS_APC_OPERATING_MODE_STATE
        )

    @property
    def supported_states(self):
        """Return supported ."""
        supported_state = [state for state in DeviceState if self.has_state(state)]
        for state in DeviceState:
            if state in supported_state:
                continue
            for sensor in self.sensors:
                if sensor.has_state(state):
                    supported_state.append(state)
                    break
        return supported_state

    def is_state_supported(self, state: DeviceState):
        """Return is supported ."""
        return state in self.supported_states

    async def update(self):
        """Update boiler state."""
        if self.client is None:
            raise CozytouchException("Unable to update boiler")
        for sensor in self.sensors:
            logger.debug("Boiler: Update sensor")
            await sensor.update()
        await super(CozytouchBoiler, self).update()
