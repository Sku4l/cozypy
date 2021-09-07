"""Utils class."""

import logging
import enum
import json
import re
from enum import Enum
from datetime import datetime

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

    def default(self, o):  # pylint: disable=arguments-differ, method-hidden
        """Transform json."""
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, CozytouchCommands):
            return {"label": o.label, "actions": o.actions}
        if isinstance(o, CozytouchAction):
            return {"deviceURL": o.device_url, "commands": o.commands}
        if isinstance(o, CozytouchCommand):
            data = {"name": o.name}
            if o.parameters is not None:
                data["parameters"] = o.parameters
            return data
        return json.JSONEncoder.default(self, o)


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


class CozytouchTimeProgram:
    """TimeProgram."""

    def __init__(self, bracket=1):
        """Initialize TimeProgram."""
        self._bracket = bracket
        self._days = [
            {"monday": []},
            {"tuesday": []},
            {"wednesday": []},
            {"thursday": []},
            {"friday": []},
            {"saturday": []},
            {"sunday": []},
        ]

    def _normalize(self):
        for day in self._days:
            for value in day.values():
                if len(value) < self._bracket:
                    for idx in range(0, 3 - len(value)):  # pylint: disable=unused-variable
                        value.append({"start": "00:00", "end": "00:00"})

    def add_day(self, day, start, end):
        """Add day."""
        for item in self._days:
            if day in item:
                item.get(day).append({"start": start, "end": end})

    def add_week(self, start, end):
        """Add day."""
        for day in self._days:
            for value in day.values():
                value.append({"start": start, "end": end})

    def get_timeprogram(self):
        """Return Timeprogram."""
        self._normalize()
        return self._days


def qualifiedname(name):
    """Return human readable name."""
    name = name.replace("APC", "Apc").replace("DHW", "Dhw").replace("MBL", "Mbl")
    name = (name.split(":"))[1]
    name = re.sub(r"(\w)([A-Z])", r"\1 \2", name)
    return name


def dt_to_json(string):
    """Convert datetime to json."""
    obj = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    if isinstance(obj, datetime.datetime):
        return {
            "year": obj.year,
            "month": obj.month,
            "day": obj.day,
            "hour": obj.hour,
            "minute": obj.minute,
            "second": obj.second,
        }
    else:
        raise TypeError("Cant serialize {}".format(obj))
