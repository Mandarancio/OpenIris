__author__ = 'martino'
from PyQt4.QtGui import QColor


class Type:
    def __init__(self, name: str, col: QColor):
        self.__name = name
        self.__color = col

    def color(self):
        return self.__color

    def name(self):
        return self.__name

    def __str__(self):
        return self.__name


class NoneType(Type):
    def __init__(self):
        Type.__init__(self, 'none', QColor(0, 102, 128))


class NumberType(Type):
    def __init__(self):
        Type.__init__(self, 'number', QColor(160, 44, 44))


class StringType(Type):
    def __init__(self):
        Type.__init__(self, 'String', QColor(33, 119, 102))