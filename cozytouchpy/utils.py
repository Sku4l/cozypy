"""Utils class."""

import logging
import enum
import json
from enum import Enum

logger = logging.getLogger(__name__)


class TextEnum(enum.Enum):
    """Text enum."""

    @classmethod
    def from_str(cls, name):
        """Enum from string."""
        for item in cls:
            if item.value == name:
                return item
        return None


class CozytouchEncoder(json.JSONEncoder):
    """Encode json."""

    def default(self, obj):  # pylint: disable=arguments-differ, method-hidden
        """Transform json."""
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, CozytouchCommands):
            return {"label": obj.label, "actions": obj.actions}
        if isinstance(obj, CozytouchAction):
            return {"deviceURL": obj.device_url, "commands": obj.commands}
        if isinstance(obj, CozytouchCommand):
            data = {"name": obj.name}
            if obj.parameters is not None:
                data["parameters"] = obj.parameters
            return data
        return json.JSONEncoder.default(self, obj)


class DeviceMetadata:
    """Metadata."""

    def __init__(self):
        """Initialize."""
        self.scheme = None
        self.device_id = None
        self.gateway_id = None
        self.entity_id = None

    @property
    def base_url(self):
        """Return base url."""
        url = self.scheme + "://" + self.gateway_id + "/" + self.device_id
        if self.entity_id is not None:
            url += "#" + self.entity_id
        return url

    def __str__(self):
        """Metadata definition."""
        return "DeviceMetadata(scheme={scheme}, device={device}, gateway={gateway},entity={entity})".format(
            scheme=self.scheme,
            device=self.device_id,
            gateway=self.gateway_id,
            entity=self.entity_id,
        )


class CozytouchCommands:
    """Commands."""

    def __init__(self, label):
        """Initialize."""
        self.label = label
        self.actions = []

    def add_action(self, action):
        """Add action."""
        self.actions.append(action)


class CozytouchAction:
    """Action."""

    def __init__(self, device_url):
        """Initialize."""
        self.device_url = device_url
        self.commands = []

    def add_command(self, command):
        """Add command."""
        self.commands.append(command)


class CozytouchCommand:
    """Command."""

    def __init__(self, name, parameters=None):
        """Initialize."""
        self.name = name
        self.parameters = parameters
        if parameters is not None and not isinstance(parameters, list):
            self.parameters = [parameters]
