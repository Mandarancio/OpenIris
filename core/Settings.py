__author__ = 'martino'
from core.UValue import BaseValue
from PyQt4.Qt import QObject
import PyQt4.QtCore as QtCore


class Setting(QObject):
    value_update = QtCore.pyqtSignal(BaseValue, object)

    def __init__(self, name: str, value: BaseValue, constant: bool=False, parent=None):
        QObject.__init__(self)
        self.__value = value
        self.__name = name
        self.__constant = constant
        self.__parent = parent

    def name(self):
        return self.__name

    def value(self):
        return self.__value.copy()

    def set_value(self, value):
        self.__value = value
        if not value.data() == self.__value.data():
            self.value_update.emit(self.__value.copy(), self.__parent)

    def is_constant(self):
        return self.__constant

    def data(self):
        return self.__value.data()

    def set_data(self, data):
        if not self.__constant:
            self.__value.set_data(data)
            # if not self.data() == data:
            self.value_update.emit(self.__value.copy(), self.__parent)

    def type(self):
        return self.__value.type()
