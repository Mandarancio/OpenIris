__author__ = 'Martino Ferrari'

from enum import Enum


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

