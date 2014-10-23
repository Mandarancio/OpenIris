__author__ = 'martino'
from core.Settings import Setting
from core.UValue import StringValue
from PyQt4.QtGui import QColor


class BlockDef:
    def __init__(self, type_name: str, name: str):
        self.settings = {"Name": Setting("Name", StringValue("Name", name))}
        self.outputs = {}
        self.inputs = {}
        self.__type_name = type_name
        self._bg_color = QColor(159, 160, 144, 255)
        self._fg_color = QColor(255, 255, 255)

    def bg_color(self):
        return self._bg_color

    def fg_color(self):
        return self._fg_color

    def type_name(self):
        return self.__type_name