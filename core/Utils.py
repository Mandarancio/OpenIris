__author__ = 'Martino Ferrari'

from enum import Enum

class Info:
	dpi=1

class Action(Enum):
    NONE = 0
    DRAG = 1
    RESIZE = 2
    CONNECTING = 3


class Mode(Enum):
    EDIT_GUI = 0
    EDIT_LOGIC = 1
    RUN = 2
    DEBUG = 3


class TriggerMode(Enum):
    AUTO = 0
    EXTERNAL = 1
    INTERNAL = 2
    BOTH = 33


class Alignment(Enum):
    Left = 0
    Right = 1
    Top = 2
    Bottom = 3
