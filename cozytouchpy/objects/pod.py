"""Describe objects for cozytouch."""
import logging

from ..constant import DeviceState
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchPod(CozytouchDevice):
    """Pod."""

    @property
    def available(self):
        """Avaiblable status."""
        return self.data["available"]

    @property
    def is_on(self):
        """Is enable."""
        return self.data["enabled"]

    @property
    def supported_states(self):
        """Supported states."""
        supported_state = [state for state in DeviceState if self.has_state(state)]
        for state in DeviceState:
            if state in supported_state:
                continue
        return supported_state

    def is_state_supported(self, state: DeviceState):
        """State."""
        return state in self.supported_states
