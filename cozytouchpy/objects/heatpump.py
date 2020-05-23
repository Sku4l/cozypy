"""Describe objects for cozytouch."""
import logging
from ..exception import CozytouchException
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchHeatPump(CozytouchDevice):
    """Heat pump."""

    @property
    def name(self):
        """Name."""
        return self.data["label"]

    async def update(self):
        """Update heating zone box."""
        if self.client is None:
            raise CozytouchException("Unable to update heat pump")
        for sensor in self.sensors:
            logger.debug("Heat Pump: Update sensor")
            await sensor.update()
        await super(CozytouchHeatPump, self).update()
