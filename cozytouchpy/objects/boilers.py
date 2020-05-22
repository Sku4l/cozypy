"""Describe objects for cozytouch."""
import logging

from ..constant import (
    DeviceCommand,
    DeviceState,
    ModeState,
)
from ..exception import CozytouchException
from .device import CozytouchDevice
from ..utils import CozytouchAction, CozytouchCommand, CozytouchCommands


logger = logging.getLogger(__name__)


class CozytouchBoiler(CozytouchDevice):
    """Boiler."""

    def __init__(self, data: dict):
        """Initialize."""
        super(CozytouchBoiler, self).__init__(data)
        self.sensors = []

    @property
    def model(self):
        """Model."""
        return self.states.get(DeviceState.PRODUCT_MODEL_NAME_STATE)

    @property
    def away_target_temperature(self):
        """Boost state."""
        return self.states.get(DeviceState.ABSENCE_HEATING_TARGET_TEMPERATURE_STATE)

    @property
    def is_on(self):
        """Is alive."""
        return self.operating_mode != ModeState.STOP

    @property
    def timeprogram_state(self):
        """Get all time program."""
        TimeProgram = {}
        for i in range(4):
            state = f"core:TimeProgram{i+1}State"
            TimeProgram.update({f"TimeProgram{i+1}": self.states.get(state)})
        return TimeProgram

    @property
    def operating_mode(self):
        """Return operation mode."""
        return self.states.get(DeviceState.PASS_APC_OPERATING_MODE_STATE)

    @property
    def operating_mode_list(self):
        """Return operating mode list."""
        return self.get_definition(DeviceState.PASS_APC_OPERATING_MODE_STATE)

    @property
    def supported_states(self) -> dict:
        """Supported states."""
        supported_states = [state for state in self.states.keys()]
        for sensor in self.sensors:
            sensor_states = [state for state in sensor.states.keys()]
            supported_states = list(set(supported_states + sensor_states))
        return supported_states

    def is_state_supported(self, state):
        """Return is supported ."""
        return state in self.supported_states

    async def set_operating_mode(self, mode):
        """Set operating mode."""
        if not self.has_state(DeviceState.PASS_APC_OPERATING_MODE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_PASS_APC_OPERATING_MODE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change operating mode")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(
            CozytouchCommand(DeviceCommand.SET_PASS_APC_OPERATING_MODE, mode)
        )
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_OPERATION_MODE))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.PASS_APC_OPERATING_MODE_STATE, mode)

    async def update(self):
        """Update boiler state."""
        if self.client is None:
            raise CozytouchException("Unable to update boiler")
        for sensor in self.sensors:
            logger.debug("Boiler: Update sensor")
            await sensor.update()
        await super(CozytouchBoiler, self).update()
