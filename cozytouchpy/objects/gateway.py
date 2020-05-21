"""Describe objects for cozytouch."""
import logging

from .place import CozytouchPlace

logger = logging.getLogger(__name__)


class CozytouchGateway:
    """Gateway."""

    def __init__(self, data: dict, place: CozytouchPlace):
        """Initialize."""
        self.data = data
        self.place = place

    @property
    def deviceUrl(self):
        """Return device url."""
        return self.data["deviceURL"]

    @property
    def id(self):
        """Return unique id."""
        return self.data["gatewayId"]

    @property
    def is_on(self):
        """Is alive."""
        return self.data["alive"]

    @property
    def version(self):
        """Return version."""
        return self.data["connectivity"]["protocolVersion"]

    @property
    def status(self):
        """Return status."""
        return self.data["connectivity"]["status"] == "OK"

    def __str__(self):
        """Definition."""
        return "Gateway(id={id},is_on={is_on},status={status}, version={version})".format(
            id=self.id, is_on=self.is_on, version=self.version, status=self.status
        )
