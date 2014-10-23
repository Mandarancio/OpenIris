__author__ = 'martino'
from core.UValue import BaseValue


class Setting:
    def __init__(self, name: str, value: BaseValue, constant: bool=False):
        self.__value = value
        self.__name = name
        self.__constant=constant

    def name(self):
        return self.__name

    def value(self):
        return self.__value.copy()

    def is_constant(self):
        return self.__constant

    def set_value(self, data):
        if not self.__constant:
            self.__value.set_data(data)