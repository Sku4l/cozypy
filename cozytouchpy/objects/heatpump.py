"""Describe objects for cozytouch."""
import logging

from cozytouchpy.constant import DeviceCommand as dc, DeviceState as ds, ThermalState
from ..exception import CozytouchException
from .device import CozytouchDevice
from ..utils import dt_to_json

logger = logging.getLogger(__name__)


class CozytouchHeatPump(CozytouchDevice):
    """Heat pump."""

    @property
    def name(self):
        """Name."""
        return self.data["label"]

    @property
    def operating_mode(self):
        """Return operation mode."""
        return self.get_state(ds.PASS_APC_OPERATING_MODE_STATE)

    @property
    def operating_mode_list(self):
        """Return operating mode list."""
        return self.get_definition(ds.PASS_APC_OPERATING_MODE_STATE)

    @property
    def away_datetime(self):
        """Return Away datetime."""
        return {
            "start": self.get_state(ds.ABSENCE_START_DATE_STATE),
            "end": self.get_state(ds.ABSENCE_END_DATE_STATE),
        }

    @property
    def away_heating_temperature(self):
        """Return operation mode."""
        return self.get_state(ds.ABSENCE_HEATING_TARGET_TEMPERATURE_STATE)

    @property
    def away_cooling_temperature(self):
        """Return operation mode."""
        return self.get_state(ds.ABSENCE_COOLING_TARGET_TEMPERATURE_STATE)

    async def set_operating_mode(self, mode):
        """Set operating mode."""
        await self.set_mode(dc.SET_PASS_APC_OPERATING_MODE, mode)

    async def set_away_datetime(self, parameters, mode):
        """Set away date time."""
        parameters = dt_to_json(parameters)
        if mode == "start":
            await self.set_mode(dc.SET_ABSENCE_START_DATE_TIME, parameters)
        if mode == "end":
            await self.set_mode(dc.SET_ABSENCE_END_DATE_TIME, parameters)

    async def set_derogate_temperature(self, temperature, thermal_mode=ThermalState.HEAT):
        """Set operating mode."""
        if thermal_mode == ThermalState.HEAT:
            await self.set_mode(dc.SET_ABSENCE_HEATING_TARGET_TEMP, temperature)
        elif thermal_mode == ThermalState.COOL:
            await self.set_mode(dc.SET_ABSENCE_COOLING_TARGET_TEMP, temperature)

    async def update(self):
        """Update heating zone box."""
        if self.client is None:
            raise CozytouchException("Unable to update heat pump")
        for sensor in self.sensors:
            logger.debug("Heat Pump: Update sensor")
            await sensor.update()
        await super(CozytouchHeatPump, self).update()
