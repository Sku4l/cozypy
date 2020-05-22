"""Describe objects for cozytouch."""
import logging
from ..constant import (
    DeviceCommand,
    DeviceState,
    DeviceType,
    OnOffState,
    ModeState,
)
from ..exception import CozytouchException

from ..utils import CozytouchAction, CozytouchCommand, CozytouchCommands
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchHeatingZone(CozytouchDevice):
    """Heating Zone Box."""

    def __init__(self, data: dict):
        """Initialize."""
        super(CozytouchHeatingZone, self).__init__(data)
        self.sensors = []

    def __get_sensors(self, device_type: DeviceType):
        for sensor in self.sensors:
            if sensor.widget == device_type:
                return sensor
        return None

    @property
    def name(self):
        """Name."""
        return self.data["label"]

    @property
    def is_on(self):
        """Heater is on."""
        return self.get_state(DeviceState.HEATING_ON_OFF_STATE) == OnOffState.ON

    @property
    def is_away(self):
        """Not implemented."""

    @property
    def state(self):
        """Return Configuration state."""
        return self.get_state(DeviceState.THERMAL_CONFIGURATION_STATE)

    @property
    def target_temperature(self):
        """Return target temperature."""
        return self.get_state(DeviceState.COMFORT_TARGET_TEMPERATURE_STATE)

    @property
    def comfort_temperature(self):
        """Return comfort temperature."""
        return self.get_state(DeviceState.COMFORT_HEATING_TARGET_TEMPERATURE_STATE)

    @property
    def eco_temperature(self):
        """Return economic temperature."""
        return self.get_state(DeviceState.ECO_HEATING_TARGET_TEMPERATURE_STATE)

    @property
    def operating_mode(self):
        """Return operation mode."""
        return ModeState.from_str(
            self.get_state(DeviceState.PASS_APC_HEATING_MODE_STATE)
        )

    def operating_mode_list(self):
        """Return operating mode list."""
        return self.get_values_definition(
            ModeState, DeviceState.PASS_APC_HEATING_MODE_STATE
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

    async def set_operating_mode(self, mode):
        """Set operating mode."""
        if not self.has_state(DeviceState.PASS_APC_HEATING_MODE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_PASS_APC_HEATING_MODE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change operating mode")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(
            CozytouchCommand(DeviceCommand.SET_PASS_APC_HEATING_MODE, mode)
        )
        action.add_command(
            CozytouchCommand(DeviceCommand.REFRESH_PASS_APC_HEATING_MODE)
        )
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.OPERATING_MODE_STATE, mode)

    async def set_eco_temperature(self, temperature):
        """Set eco temperature."""
        if not self.has_state(DeviceState.ECO_HEATING_TARGET_TEMPERATURE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_ECO_HEATING_TARGET_TEMPERATURE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        commands = CozytouchCommands("Set eco temperature")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(
            CozytouchCommand(
                DeviceCommand.SET_ECO_HEATING_TARGET_TEMPERATURE, temperature
            )
        )
        action.add_command(
            CozytouchCommand(DeviceCommand.REFRESH_ECO_HEATING_TARGET_TEMPERATURE)
        )
        commands.add_action(action)
        await self.client.send_commands(commands)
        self.set_state(DeviceState.ECO_HEATING_TARGET_TEMPERATURE_STATE, temperature)

    async def set_comfort_temperature(self, temperature):
        """Set comfort temperature."""
        if not self.has_state(DeviceState.COMFORT_HEATING_TARGET_TEMPERATURE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_COMFORT_HEATING_TARGET_TEMPERATURE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        commands = CozytouchCommands("Set comfort temperature")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(
            CozytouchCommand(
                DeviceCommand.SET_COMFORT_HEATING_TARGET_TEMPERATURE, temperature
            )
        )
        action.add_command(
            CozytouchCommand(DeviceCommand.REFRESH_COMFORT_HEATING_TARGET_TEMPERATURE)
        )
        commands.add_action(action)
        await self.client.send_commands(commands)
        self.set_state(
            DeviceState.COMFORT_HEATING_TARGET_TEMPERATURE_STATE, temperature
        )

    async def turn_on(self):
        """Set on."""
        if not self.has_state(DeviceState.HEATING_ON_OFF_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_HEATING_ON_OFF_STATE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        commands = CozytouchCommands("Set Heating mode ON")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(
            CozytouchCommand(DeviceCommand.SET_HEATING_ON_OFF_STATE, OnOffState.ON)
        )
        commands.add_action(action)
        await self.client.send_commands(commands)
        self.set_state(DeviceState.HEATING_ON_OFF_STATE, OnOffState.ON)

    async def turn_off(self):
        """Set off."""
        if not self.has_state(DeviceState.HEATING_ON_OFF_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_HEATING_ON_OFF_STATE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        commands = CozytouchCommands("Set Heating mode ON")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(
            CozytouchCommand(DeviceCommand.SET_HEATING_ON_OFF_STATE, OnOffState.ON)
        )
        commands.add_action(action)
        await self.client.send_commands(commands)
        self.set_state(DeviceState.HEATING_ON_OFF_STATE, OnOffState.ON)

    async def update(self):
        """Update heating zone box."""
        if self.client is None:
            raise CozytouchException("Unable to update heating zone box")
        for sensor in self.sensors:
            logger.debug("Heating Zone: Update sensor")
            await sensor.update()
        await super(CozytouchHeatingZone, self).update()
