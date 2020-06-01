"""Describe objects for cozytouch."""
import logging

from ..constant import (
    DeviceCommand as dc,
    DeviceState as ds,
    DeviceType as dt,
    ModeState,
    OnOffState,
)
from ..exception import CozytouchException
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
        if self.widget == dt.PILOT_WIRE_INTERFACE:
            return self.target_heating_level != ModeState.OFF
        elif self.widget == dt.HEATER:
            return self.operating_mode != ModeState.STANDBY
        elif self.widget == dt.APC_HEATING_ZONE:
            return self.operating_mode != ModeState.STOP
        return False

    @property
    def is_away(self):
        """Heater is away."""
        away = self.get_state(ds.AWAY_STATE)
        if away is None:
            return False
        return True if away == "on" else False

    @property
    def is_heating(self):
        """Heater is heating."""
        return self.get_state(ds.PASS_APC_HEATING_MODE_STATE) == OnOffState.ON

    @property
    def is_cooling(self):
        """Heater is heating."""
        return self.get_state(ds.PASS_APC_COOLING_MODE_STATE) == OnOffState.ON

    @property
    def temperature(self):
        """Return temperature."""
        sensor = self.get_sensors(dt.TEMPERATURE)
        if sensor is None:
            return 0
        return sensor.temperature

    @property
    def thermal_state(self):
        """Return Thermal state."""
        return self.get_state(ds.THERMAL_CONFIGURATION_STATE)

    @property
    def target_temperature(self):
        """Return target temperature."""
        if self.widget == dt.APC_HEATING_ZONE:
            return self.get_state(ds.COMFORT_TARGET_TEMPERATURE_STATE)
        return self.get_state(ds.TARGET_TEMPERATURE_STATE)

    @property
    def target_comfort_temperature(self):
        """Return comfort temperature."""
        if self.widget == dt.APC_HEATING_ZONE:
            return self.get_state(ds.COMFORT_HEATING_TARGET_TEMPERATURE_STATE)
        return self.get_state(ds.COMFORT_TEMPERATURE_STATE)

    @property
    def target_comfort_cooling_temperature(self):
        """Return comfort temperature."""
        if self.widget == dt.APC_HEATING_COOLING_ZONE:
            return self.get_state(ds.COMFORT_COOLING_TARGET_TEMPERATURE_STATE)
        return None

    @property
    def target_eco_temperature(self):
        """Return economic temperature."""
        if self.widget == dt.APC_HEATING_ZONE:
            return self.get_state(ds.ECO_HEATING_TARGET_TEMPERATURE_STATE)

        comfort_temp = self.target_comfort_temperature
        if comfort_temp is None:
            return 0
        return comfort_temp - self.get_state(ds.ECO_TEMPERATURE_STATE)

    @property
    def operating_mode(self):
        """Return operation mode."""
        if self.widget == dt.APC_HEATING_ZONE:
            return self.get_state(ds.PASS_APC_HEATING_MODE_STATE)
        return self.get_state(ds.OPERATING_MODE_STATE)

    @property
    def operating_mode_list(self):
        """Return operating mode list."""
        if self.widget == dt.APC_HEATING_ZONE:
            return self.get_definition(ds.PASS_APC_HEATING_MODE_STATE)
        return self.get_definition(ds.OPERATING_MODE_STATE)

    @property
    def cooling_operating_mode_list(self):
        """Return operating mode list."""
        if self.widget == dt.APC_HEATING_COOLING_ZONE:
            return self.get_definition(ds.PASS_APC_COOLING_MODE_STATE)
        return None

    @property
    def target_heating_level(self):
        """Return heating level."""
        return self.get_state(ds.TARGETING_HEATING_LEVEL_STATE)

    @property
    def target_heating_level_list(self):
        """Return heating level list."""
        return self.get_definition(ds.TARGETING_HEATING_LEVEL_STATE)

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
        mode_state = ds.OPERATING_MODE_STATE
        actions = [(dc.SET_OPERATION_MODE, mode), (dc.REFRESH_OPERATION_MODE, None)]
        if self.widget == dt.APC_HEATING_ZONE:
            mode_state = ds.PASS_APC_HEATING_MODE_STATE
            actions = [
                (dc.SET_PASS_APC_HEATING_MODE, mode),
                (dc.REFRESH_PASS_APC_HEATING_MODE, None),
            ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, mode)

    async def set_targeting_heating_level(self, level):
        """Set targeting heating level."""
        mode_state = ds.TARGETING_HEATING_LEVEL_STATE
        actions = [(dc.SET_HEATING_LEVEL, level)]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, level)

    async def set_eco_temperature(self, temp):
        """Set eco temperature."""
        mode_state = ds.ECO_TEMPERATURE_STATE
        temperature = float(self.target_comfort_temperature) - float(temp)
        actions = [
            (dc.SET_ECO_TEMP, temperature),
            (dc.REFRESH_LOWERING_TEMP_PROG, None),
        ]

        if self.widget == dt.APC_HEATING_ZONE:
            mode_state = ds.ECO_HEATING_TARGET_TEMPERATURE_STATE
            temperature = temp
            actions = [
                (dc.SET_ECO_HEATING_TARGET_TEMPERATURE, temperature),
                (dc.REFRESH_ECO_HEATING_TARGET_TEMPERATURE, None),
            ]

        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)

    async def set_comfort_temperature(self, temperature):
        """Set comfort temperature."""
        mode_state = ds.COMFORT_TEMPERATURE_STATE
        eco_state = ds.ECO_TEMPERATURE_STATE
        eco_temp = float(temperature) - float(self.target_eco_temperature)
        actions = [
            (dc.SET_COMFORT_TEMP, temperature),
            (dc.SET_ECO_TEMP, eco_temp),
            (dc.REFRESH_TARGET_TEMPERATURE, None),
            (dc.REFRESH_COMFORT_TEMPERATURE, None),
            (dc.REFRESH_LOWERING_TEMP_PROG, None),
        ]

        if self.widget == dt.APC_HEATING_ZONE:
            mode_state = ds.COMFORT_HEATING_TARGET_TEMPERATURE_STATE
            eco_state = ds.ECO_HEATING_TARGET_TEMPERATURE_STATE
            eco_temp = float(self.target_eco_temperature)
            actions = [
                (dc.SET_COMFORT_HEATING_TARGET_TEMPERATURE, temperature),
                (dc.REFRESH_COMFORT_HEATING_TARGET_TEMPERATURE, None),
            ]

        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)
        self.set_state(eco_state, eco_temp)

    async def set_target_temperature(self, temperature):
        """Set target temperature."""
        mode_state = ds.TARGET_TEMPERATURE_STATE
        actions = [
            (dc.SET_TARGET_TEMP, temperature),
            (dc.REFRESH_ECO_TEMPERATURE, None),
            (dc.REFRESH_COMFORT_TEMPERATURE, None),
            (dc.REFRESH_LOWERING_TEMP_PROG, None),
        ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)

    async def set_heating_mode(self, mode):
        """Set heating."""
        mode_state = ds.PASS_APC_HEATING_MODE_STATE
        actions = [
            (dc.SET_PASS_APC_HEATING_MODE, mode),
            (dc.REFRESH_PASS_APC_HEATING_MODE, None),
        ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, mode)

    async def set_away_mode(self, mode: OnOffState):
        """Set away mode off."""
        mode_state = ds.AWAY_STATE
        actions = [(dc.SET_AWAY_MODE, mode)]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, mode)

    async def turn_away_mode_on(self):
        """Turn on away mode."""
        if self.widget == dt.APC_HEATING_ZONE:
            await self.set_targeting_heating_level(ModeState.ABSENCE)
        else:
            await self.set_away_mode(OnOffState.ON)

    async def turn_away_mode_off(self):
        """Turn off away mode."""
        if self.widget == dt.APC_HEATING_ZONE:
            await self.set_targeting_heating_level(ModeState.STOP)
        else:
            await self.set_away_mode(OnOffState.OFF)

    async def turn_on(self):
        """Set on."""
        if self.widget == dt.PILOT_WIRE_INTERFACE:
            await self.set_targeting_heating_level(ModeState.COMFORT)
        elif self.widget == dt.HEATER:
            await self.set_operating_mode(ModeState.INTERNAL)
        elif self.widget == dt.APC_HEATING_ZONE:
            mode_state = ds.HEATING_ON_OFF_STATE
            actions = [(dc.SET_HEATING_ON_OFF_STATE, OnOffState.ON)]
            await self.set_mode(mode_state, actions)

    async def turn_off(self):
        """Set off."""
        if self.widget == dt.PILOT_WIRE_INTERFACE:
            await self.set_targeting_heating_level(ModeState.OFF)
        elif self.widget == dt.HEATER:
            await self.set_operating_mode(ModeState.STANDBY)
        elif self.widget == dt.APC_HEATING_ZONE:
            mode_state = ds.HEATING_ON_OFF_STATE
            actions = [(dc.SET_HEATING_ON_OFF_STATE, OnOffState.OFF)]
            await self.set_mode(mode_state, actions)

    async def update(self):
        """Update heater device."""
        if self.client is None:
            raise CozytouchException("Unable to update heater")
        for sensor in self.sensors:
            logger.debug("Heater : Update sensor")
            await sensor.update()
        await super(CozytouchHeater, self).update()
