import logging
import enum
import json
from enum import Enum

logger = logging.getLogger(__name__)


class TextEnum(enum.Enum):
    @classmethod
    def from_str(cls, name):
        for item in cls:
            if item.value == name:
                return item
        return None


class CozytouchEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=arguments-differ, method-hidden
        from .objects import CozytouchCommands, CozytouchAction, CozytouchCommand

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
