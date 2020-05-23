"""Describe objects for cozytouch."""
import logging

from ..constant import DeviceCommand, DeviceState, ModeState, OnOffState, DeviceType
from ..exception import CozytouchException
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchWaterHeater(CozytouchDevice):
    """Water Heater."""

    @property
    def is_on(self):
        """Is alive."""
        return self.operating_mode != ModeState.STANDBY

    @property
    def operating_mode(self):
        """Return operation mode."""
        if self.widget == DeviceType.APC_WATER_HEATER:
            return self.get_state(DeviceState.PASS_APC_DHW_MODE_STATE)
        return self.get_state(DeviceState.DHW_MODE_STATE)

    @property
    def operating_mode_list(self):
        """Return operating mode list."""
        if self.widget == DeviceType.APC_WATER_HEATER:
            return self.get_definition(DeviceState.PASS_APC_DHW_MODE_STATE)
        return self.get_definition(DeviceState.DHW_MODE_STATE)

    @property
    def current_temperature(self):
        """Return tempereture (middle water heater)."""
        return self.get_state(DeviceState.MIDDLE_WATER_TEMPERATURE_STATE)

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        if self.widget == DeviceType.APC_WATER_HEATER:
            return self.get_definition(DeviceState.TARGET_DHW_TEMPERATURE_STATE)
        return self.get_state(DeviceState.TARGET_TEMPERATURE_STATE)

    @property
    def is_away_mode_on(self):
        """Return true if away mode is on."""
        return self.get_state(DeviceState.OPERATING_MODE_STATE) == OnOffState.ON

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
        mode_state = DeviceState.OPERATING_MODE_STATE
        actions = [
            {"action": DeviceCommand.SET_DWH_MODE, "value": mode},
            {"action": DeviceCommand.REFRESH_DHW_MODE},
        ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, mode)

    async def set_away_mode(self, duration):
        """Set away mode."""
        mode_state = DeviceState.AWAY_MODE_DURATION_STATE
        if int(duration) == 0:
            actions = [
                {
                    "action": DeviceCommand.SET_CURRENT_OPERATING_MODE,
                    "value": {"relaunch": "off", "absence": "off"},
                }
            ]
            await self.set_mode(mode_state, actions)
        else:
            actions = [
                {"action": DeviceCommand.SET_AWAYS_MODE_DURATION, "value": duration},
                {
                    "action": DeviceCommand.SET_CURRENT_OPERATING_MODE,
                    "value": {"relaunch": "off", "absence": "on"},
                },
                {"action": DeviceCommand.REFRESH_AWAYS_MODE_DURATION},
            ]
            await self.set_mode(mode_state, actions)

    async def set_boost_mode(self, duration):
        """Set Boost mode."""
        if self.widget == DeviceType.APC_WATER_HEATER:
            mode_state = DeviceState.BOOST_ON_OFF_STATE
            if int(duration) == 0:
                actions = [
                    {
                        "action": DeviceCommand.SET_BOOST_MODE_DURATION,
                        "value": OnOffState.OFF,
                    }
                ]
                await self.set_mode(mode_state, actions)
                self.set_state(mode_state, OnOffState.OFF)
            else:
                actions = [
                    {
                        "action": DeviceCommand.SET_BOOST_MODE_DURATION,
                        "value": OnOffState.ON,
                    }
                ]
                await self.set_mode(mode_state, actions)
                self.set_state(mode_state, OnOffState.ON)
        else:
            mode_state = DeviceState.BOOST_MODE_DURATION_STATE
            if int(duration) == 0:
                actions = [
                    {
                        "action": DeviceCommand.SET_CURRENT_OPERATING_MODE,
                        "value": {"relaunch": "off", "absence": "off"},
                    }
                ]
                await self.set_mode(mode_state, actions)
                self.set_state(mode_state, duration)
            else:
                actions = [
                    {
                        "action": DeviceCommand.SET_BOOST_MODE_DURATION,
                        "value": duration,
                    },
                    {
                        "action": DeviceCommand.SET_CURRENT_OPERATING_MODE,
                        "value": {"relaunch": "on", "absence": "off"},
                    },
                    {"action": DeviceCommand.REFRESH_BOOST_MODE_DURATION},
                ]
                await self.set_mode(mode_state, actions)
                self.set_state(mode_state, duration)

    async def set_temperature(self, temperature):
        """Set temperature."""
        mode_state = DeviceState.TARGET_TEMPERATURE_STATE
        actions = [
            {"action": DeviceCommand.SET_TARGET_TEMP, "value": temperature},
            {"action": DeviceCommand.REFRESH_TARGET_TEMPERATURE},
        ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)

    async def set_eco_temperature(self, temperature):
        """Set operating mode."""
        mode_state = DeviceState.ECO_TARGET_DHW_TEMPERATURE_STATE
        actions = [
            {
                "action": DeviceCommand.SET_ECO_TARGET_DHW_TEMPERATURE,
                "value": temperature,
            },
            {"action": DeviceCommand.REFRESH_ECO_TARGET_DHW_TEMPERATURE},
        ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)

    async def set_comfort_temperature(self, temperature):
        """Set operating mode."""
        mode_state = DeviceState.COMFORT_TARGET_DHW_TEMPERATURE_STATE
        actions = [
            {
                "action": DeviceCommand.SET_COMFORT_TARGET_DHW_TEMPERATURE,
                "value": temperature,
            },
            {"action": DeviceCommand.REFRESH_COMFORT_TARGET_DHW_TEMPERATURE},
        ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)

    async def update(self):
        """Update water heater ."""
        if self.client is None:
            raise CozytouchException("Unable to update heater")
        for sensor in self.sensors:
            logger.debug("Water Heater : Update sensor")
            await sensor.update()
        await super(CozytouchWaterHeater, self).update()
