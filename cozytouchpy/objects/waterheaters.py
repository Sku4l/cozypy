"""Describe objects for cozytouch."""
import logging

from ..constant import (
    DeviceCommand,
    DeviceState,
    DeviceType,
    ModeState,
)
from ..exception import CozytouchException

from ..utils import CozytouchAction, CozytouchCommand, CozytouchCommands
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchWaterHeater(CozytouchDevice):
    """Water Heater."""

    def __init__(self, data: dict):
        """Initialize."""
        super(CozytouchWaterHeater, self).__init__(data)
        self.sensors = []

    def __get_sensors(self, device_type: DeviceType):
        for sensor in self.sensors:
            if sensor.widget == device_type:
                return sensor
        return None

    @property
    def is_on(self):
        """Is alive."""
        return self.operating_mode != ModeState.STANDBY

    @property
    def operating_mode(self):
        """Return operation mode."""
        return ModeState.from_str(self.get_state(DeviceState.OPERATING_MODE_STATE))

    @property
    def operating_mode_list(self):
        """Return operating mode list."""
        return self.get_values_definition(ModeState, DeviceState.OPERATING_MODE_STATE)

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

    async def set_operating_mode(self, mode):
        """Set operating mode."""
        if not self.has_state(DeviceState.OPERATING_MODE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_DWH_MODE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change operating mode")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(CozytouchCommand(DeviceCommand.SET_DWH_MODE, mode))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_DHW_MODE))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.OPERATING_MODE_STATE, mode)

    async def set_away_mode(self, duration):
        """Set away mode."""
        if not self.has_state(DeviceState.AWAY_MODE_DURATION_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_DWH_MODE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change operating mode")
        action = CozytouchAction(device_url=self.deviceUrl)
        if int(duration) == 0:
            action.add_command(
                CozytouchCommand(
                    DeviceCommand.SET_CURRENT_OPERATION_MODE,
                    {"relaunch": "off", "absence": "off"},
                )
            )
        else:
            action.add_command(
                CozytouchCommand(
                    DeviceCommand.SET_CURRENT_OPERATION_MODE,
                    {"relaunch": "off", "absence": "on"},
                )
            )
        action.add_command(
            CozytouchCommand(DeviceCommand.SET_AWAYS_MODE_DURATION, duration)
        )
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_AWAYS_MODE_DURATION))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.AWAY_MODE_DURATION_STATE, duration)

    async def set_boost_mode(self, duration):
        """Set Boost mode."""
        if not self.has_state(DeviceState.BOOST_MODE_DURATION_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_BOOST_MODE_DURATION
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change Boost mode")
        action = CozytouchAction(device_url=self.deviceUrl)
        if int(duration) == 0:
            action.add_command(
                CozytouchCommand(
                    DeviceCommand.SET_CURRENT_OPERATION_MODE,
                    {"relaunch": "off", "absence": "off"},
                )
            )
        else:
            action.add_command(
                CozytouchCommand(
                    DeviceCommand.SET_CURRENT_OPERATION_MODE,
                    {"relaunch": "on", "absence": "off"},
                )
            )
            action.add_command(
                CozytouchCommand(DeviceCommand.SET_BOOST_MODE_DURATION, duration)
            )
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_BOOST_MODE_DURATION))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.BOOST_MODE_DURATION_STATE, duration)

    async def set_temperature(self, temp):
        """Set temperature."""
        if not self.has_state(DeviceState.TARGET_TEMPERATURE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_TARGET_TEMP
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change target temperature")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(CozytouchCommand(DeviceCommand.SET_TARGET_TEMP, temp))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_TARGET_TEMPERATURE))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.TARGET_TEMPERATURE_STATE, temp)

    async def update(self):
        """Update water heater ."""
        if self.client is None:
            raise CozytouchException("Unable to update heater")
        for sensor in self.sensors:
            logger.debug("Water Heater : Update sensor")
            await sensor.update()
        await super(CozytouchWaterHeater, self).update()
