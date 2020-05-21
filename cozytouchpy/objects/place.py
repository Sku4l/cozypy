"""Describe objects for cozytouch."""
import logging

from .object import CozytouchObject

logger = logging.getLogger(__name__)


class CozytouchPlace(CozytouchObject):
    """Place."""

    def __str__(self):
        """Definition."""
        return "Place(id={id},name={name})".format(id=self.id, name=self.name)
