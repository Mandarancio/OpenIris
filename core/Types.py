__author__ = 'martino'
from PyQt4.QtGui import QColor, QLabel, QSpinBox, QComboBox


class Type:
    def __init__(self, name: str, col: QColor):
        self.__name = name
        self.__color = col

    def color(self):
        return self.__color

    def name(self):
        return self.__name

    def compatible(self, other):
        if other.name() == self.__name:
            return True
        return False

    def __str__(self):
        return self.__name

    @staticmethod
    def edit_widget(v):
        return QLabel(str(v))


class TypeOfType(Type):
    def __init__(self):
        Type.__init__(self, 'type', QColor(125, 125, 125))

    @staticmethod
    def edit_widget(v):
        return QComboBox()


class NoneType(Type):
    def __init__(self):
        Type.__init__(self, 'none', QColor(0, 102, 128))

    def compatible(self, other):
        return True

    @staticmethod
    def edit_widget(v):
        return QSpinBox(v)


class NumberType(Type):
    def __init__(self, name: str='number'):
        Type.__init__(self, name, QColor(160, 44, 44))

    def compatible(self, other):
        if issubclass(other.__class__, NumberType):
            return True
        return False


class IntegerType(NumberType):
    def __init__(self):
        NumberType.__init__(self, 'integer')


class FloatType(NumberType):
    def __init__(self):
        NumberType.__init__(self, 'float')


class StringType(Type):
    def __init__(self):
        Type.__init__(self, 'String', QColor(33, 119, 102))