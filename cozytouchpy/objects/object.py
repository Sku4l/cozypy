"""Describe objects for cozytouch."""
import logging

logger = logging.getLogger(__name__)


class CozytouchObject:
    """Object."""

    def __init__(self, data: dict):
        """Initialize."""
        self.client = None
        self.data = data

    @property
    def id(self):
        """Return Unique id."""
        return self.data["oid"]

    @property
    def name(self):
        """Name."""
        return self.data["label"]

    @property
    def creationTime(self):
        """Creation datetime."""
        return self.data["creationTime"]

    @property
    def lastUpdateTime(self):
        """Last update."""
        return self.data["lastUpdateTime"]
