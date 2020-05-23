"""Describe objects for cozytouch."""
import logging

from ..constant import (
    DeviceCommand,
    DeviceState,
    DeviceType,
    ModeState,
    OnOffState,
)
from ..exception import CozytouchException

from ..utils import CozytouchAction, CozytouchCommand, CozytouchCommands
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchHeater(CozytouchDevice):
    """Heater."""

    @property
    def name(self):
        """Name."""
        return self.data["label"]

    @property
    def is_on(self):
        """Heater is on."""
        if self.widget == DeviceType.PILOT_WIRE_INTERFACE:
            return self.target_heating_level != ModeState.OFF
        elif self.widget == DeviceType.HEATER:
            return self.operating_mode != ModeState.STANDBY
        return False

    @property
    def is_away(self):
        """Heater is away."""
        away = self.get_state(DeviceState.AWAY_STATE)
        if away is None:
            return False
        return True if away == "on" else False

    @property
    def temperature(self):
        """Return temperature."""
        sensor = self.get_sensors(DeviceType.TEMPERATURE)
        if sensor is None:
            return 0
        return sensor.temperature

    @property
    def target_temperature(self):
        """Return target temperature."""
        return self.get_state(DeviceState.TARGET_TEMPERATURE_STATE)

    @property
    def comfort_temperature(self):
        """Return comfort temperature."""
        return self.get_state(DeviceState.COMFORT_TEMPERATURE_STATE)

    @property
    def eco_temperature(self):
        """Return economic temperature."""
        comfort_temp = self.comfort_temperature
        if comfort_temp is None:
            return 0
        return comfort_temp - self.get_state(DeviceState.ECO_TEMPERATURE_STATE)

    @property
    def operating_mode(self):
        """Return operation mode."""
        return self.get_state(DeviceState.OPERATING_MODE_STATE)

    @property
    def operating_mode_list(self):
        """Return operating mode list."""
        return self.get_definition(DeviceState.OPERATING_MODE_STATE)

    @property
    def target_heating_level(self):
        """Return heating level."""
        return self.get_state(DeviceState.TARGETING_HEATING_LEVEL_STATE)

    @property
    def target_heating_level_list(self):
        """Return heating level list."""
        return self.get_definition(DeviceState.TARGETING_HEATING_LEVEL_STATE)

    @property
    def supported_states(self) -> dict:
        """Supported states."""
        supported_states = [state["name"] for state in self.states]
        for sensor in self.sensors:
            sensor_states = [state["name"] for state in sensor.states]
            supported_states = list(set(supported_states + sensor_states))
        return supported_states

    def is_state_supported(self, state):
        """Is supported ."""
        return state in self.supported_states

    async def set_operating_mode(self, mode):
        """Set operating mode."""
        if not self.has_state(DeviceState.OPERATING_MODE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_OPERATION_MODE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change operating mode")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(CozytouchCommand(DeviceCommand.SET_OPERATION_MODE, mode))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_OPERATION_MODE))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.OPERATING_MODE_STATE, mode)

    async def set_targeting_heating_level(self, level):
        """Set targeting heating level."""
        if not self.has_state(DeviceState.TARGETING_HEATING_LEVEL_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_HEATING_LEVEL
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change heating level")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(CozytouchCommand(DeviceCommand.SET_HEATING_LEVEL, level))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.TARGETING_HEATING_LEVEL_STATE, level)

    async def set_eco_temperature(self, temp):
        """Set eco temperature."""
        if not self.has_state(DeviceState.ECO_TEMPERATURE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_ECO_TEMP
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        temperature = self.comfort_temperature - temp

        commands = CozytouchCommands("Set eco temperature")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(CozytouchCommand(DeviceCommand.SET_ECO_TEMP, temperature))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_LOWERING_TEMP_PROG))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.ECO_TEMPERATURE_STATE, temperature)

    async def set_comfort_temperature(self, temperature):
        """Set comfort temperature."""
        if not self.has_state(DeviceState.COMFORT_TEMPERATURE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_COMFORT_TEMP
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        eco_temp = temperature - self.eco_temperature

        commands = CozytouchCommands("Set comfort temperature")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(
            CozytouchCommand(DeviceCommand.SET_COMFORT_TEMP, temperature)
        )
        action.add_command(CozytouchCommand(DeviceCommand.SET_ECO_TEMP, eco_temp))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_LOWERING_TEMP_PROG))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_TARGET_TEMPERATURE))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.COMFORT_TEMPERATURE_STATE, temperature)
        self.set_state(DeviceState.ECO_TEMPERATURE_STATE, eco_temp)

    async def set_target_temperature(self, temperature):
        """Set target temperature."""
        if not self.has_state(DeviceState.TARGET_TEMPERATURE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_TARGET_TEMP
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Set eco temperature")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(CozytouchCommand(DeviceCommand.SET_TARGET_TEMP, temperature))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_ECO_TEMPERATURE))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_COMFORT_TEMPERATURE))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_LOWERING_TEMP_PROG))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.TARGET_TEMPERATURE_STATE, temperature)

    async def turn_away_mode_off(self):
        """Set away mode off."""
        if not self.has_state(DeviceState.AWAY_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_AWAY_MODE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Set away mode OFF")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(
            CozytouchCommand(DeviceCommand.SET_AWAY_MODE, OnOffState.OFF)
        )
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.AWAY_STATE, OnOffState.OFF)

    async def turn_away_mode_on(self):
        """Set away mode on."""
        if not self.has_state(DeviceState.AWAY_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(
                    command=DeviceCommand.SET_AWAY_MODE
                )
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Set away mode ON")
        action = CozytouchAction(device_url=self.deviceUrl)
        action.add_command(CozytouchCommand(DeviceCommand.SET_AWAY_MODE, OnOffState.ON))
        commands.add_action(action)

        await self.client.send_commands(commands)

        self.set_state(DeviceState.AWAY_STATE, OnOffState.ON)

    async def turn_on(self):
        """Set on."""
        if self.widget == DeviceType.PILOT_WIRE_INTERFACE:
            await self.set_targeting_heating_level(ModeState.COMFORT)
        elif self.widget == DeviceType.HEATER:
            await self.set_operating_mode(ModeState.INTERNAL)

    async def turn_off(self):
        """Set off."""
        if self.widget == DeviceType.PILOT_WIRE_INTERFACE:
            await self.set_targeting_heating_level(ModeState.OFF)
        elif self.widget == DeviceType.HEATER:
            await self.set_operating_mode(ModeState.STANDBY)

    async def update(self):
        """Update heater device."""
        if self.client is None:
            raise CozytouchException("Unable to update heater")
        for sensor in self.sensors:
            logger.debug("Heater : Update sensor")
            await sensor.update()
        await super(CozytouchHeater, self).update()
