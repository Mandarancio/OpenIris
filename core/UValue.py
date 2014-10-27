""" @package UValue
This module provide a simple system of universally compatible Value class
"""
__author__ = 'martino'

import math
import sys

from core.SIUnit import NoUnit, Unit
from core.Types import *


class BaseValue:
    """
    "Abstract" universal value class (to not be used)
    """

    def __init__(self, name: str, type_name: Type, data=None):
        """
        Constructor of BaseValue
        :param name: Name of the value (or variable)
        :param type_name: Type name
        :param data: data to be stored
        """
        self._name = name
        self._type = type_name
        self._numerical = False
        self._data = data

    def set_name(self, name: str):
        """
        Change the name of the value
        :param name: new name
        """
        self._name = name

    def name(self):
        """
        Get the name of this value
        :return: the name of the value
        """
        return self._name

    def numerical(self):
        """
        Check if this value is a numerical value or not
        :return: True if is numerical, False in other case
        """
        return self._numerical

    def type(self):
        """
        Get type name
        :return: type name (as str)
        """
        return self._type

    def data(self):
        """
        Get the stored data
        :return: the stored data
        """
        return self._data

    def set_data(self, data):
        """
        Store a new data
        :param data: the new data
        """
        if self._check_data(data):
            self._data = data

    @staticmethod
    def clone(name: str, data):
        """
        Clone the current class
        :param name: name of the new Value
        :param data: data to be stored in the new Value
        :return: the new Value
        """
        return BaseValue(name, NoneType(), data)

    @staticmethod
    def parse(s: str):
        return None

    def copy(self):
        return BaseValue(self._name, self._type, self._data)

    def _check_data(self, data):
        """
        Check if the data is compatible
        :param data: the data to be checked
        :return: if data is compatible
        """
        return True

    def compatible(self, other):
        """
        Check if two Value are compatibles
        :param other: the other Value object
        :return: if they are compatibles
        """
        if other.type() == self.type():
            return True
        return False

    def __str__(self):
        return self._type + "(" + self._name + " : " + str(self._data) + ")"


class NumericalValue(BaseValue):
    """
    "Abstract" class for managing numerical values
    """

    def __init__(self, name: str, sub_type: Type, val, unit: Unit=NoUnit(), v_min=float('nan'), v_max=float('nan')):
        """
        Constructor for NumericalValue
        :param name: Name of the value
        :param val: Numerical value
        :param unit: Unit of the value (optional, by default NoUnit)
        """
        BaseValue.__init__(self, name, sub_type, val)
        self._numerical = True
        self.max = v_max
        self.min = v_min
        self.unit = unit

    def _check_margin(self, data):
        """
        Check if data is inside the set max and min margins (if they are defined)
        :param data: data to check
        :return: if is inside the margins
        """
        if not math.isnan(self.max) and self.max < data:
            return False
        if not math.isnan(self.min) and self.min > data:
            return False
        return True

    def compatible(self, other):
        if other.numerical():
            return True
        return False

    def copy(self):
        return NumericalValue(self._name, self._type, self._data, unit=Unit, v_min=self.min, v_max=self.max)

    def __str__(self):
        return self.unit.print(self.data())

    def __add__(self, other):
        if self.compatible(other):
            if isinstance(self, IntegerValue) and isinstance(other, IntegerValue):
                v = IntegerValue.clone(self._name + '+' + other.name(), self.data() + other.data())
            else:
                v = FloatValue.clone(self._name + '+' + other.name(), float(self.data()) + float(other.data()))
            if self.unit.name() == other.unit.name():
                v.unit = self.unit
            else:
                v.unit = NoUnit()
            return v

    def __sub__(self, other):
        if self.compatible(other):
            if isinstance(self, IntegerValue) and isinstance(other, IntegerValue):
                v = IntegerValue.clone(self._name + '-' + other.name(), self.data() - other.data())
            else:
                v = FloatValue.clone(self._name + '-' + other.name(), float(self.data()) - float(other.data()))
            if self.unit.name() == other.unit.name():
                v.unit = self.unit
            else:
                v.unit = NoUnit()
            return v

    def __mul__(self, other):
        if self.compatible(other):
            if isinstance(self, IntegerValue) and isinstance(other, IntegerValue):
                v = IntegerValue.clone(self._name + '-' + other.name(), self.data() * other.data())
            else:
                v = FloatValue.clone(self._name + '-' + other.name(), float(self.data()) * float(other.data()))
            v.unit = self.unit * other.unit
            return v

    def __truediv__(self, other):
        if self.compatible(other):
            if isinstance(self, IntegerValue) and isinstance(other, IntegerValue):
                v = IntegerValue.clone(self._name + '/' + other.name(), self.data() / other.data())
            else:
                v = FloatValue.clone(self._name + '/' + other.name(), float(self.data()) / float(other.data()))
            v.unit = self.unit / other.unit
            return v

    def __floordiv__(self, other):
        if self.compatible(other):
            v = IntegerValue.clone(self._name + '//' + other.name(), self.data() // other.data())
            v.unit = self.unit / other.unit
            return v


class IntegerValue(NumericalValue):
    """IntegerValue class, to store and manipulate Int values"""

    def __init__(self, name: str, val: int, v_min: int=-sys.maxsize, v_max: int=sys.maxsize, unit: Unit=NoUnit()):
        """
        Constructor for IntegerValue
        :param name: Name of the value
        :param val: Integer value
        :param v_min: Minimum value (optional, by default - maxsize)
        :param v_max: Maximum value (optional, by default + maxsize)
        :param unit: Unit of the value (optional, by default NoUnit)
        """
        NumericalValue.__init__(self, name, NumberType(), val, unit=unit, v_min=v_min, v_max=v_max)
        self._data = int(self._data)

    def _check_data(self, data):
        if isinstance(data, int):
            return self._check_margin(data)
        if isinstance(data, float):
            return self._check_margin(int(data))
        return False

    def set_data(self, data):
        if self._check_data(data):
            self._data = int(data)

    @staticmethod
    def clone(name: str, val):
        return IntegerValue(name, val)

    def copy(self):
        return IntegerValue(self._name, self._data, unit=self.unit, v_max=int(self.max), v_min=int(self.min))

    @staticmethod
    def parse(s: str):
        if s.find('.') != -1:
            return None
        try:
            v = int(s)
            return IntegerValue('Int', v)
        except ValueError:
            return None


class FloatValue(NumericalValue):
    def __init__(self, name: str, val: float, v_min: float=float('nan'), v_max: float=float('nan'),
                 unit: Unit=NoUnit()):
        NumericalValue.__init__(self, name, NumberType(), val, unit=unit, v_min=v_min, v_max=v_max)
        self._data = float(self._data)

    def _check_data(self, data):
        if isinstance(data, int) or isinstance(data, float):
            return self._check_margin(data)
        return False

    def set_data(self, data):
        if self._check_data(data):
            self._data = float(data)

    @staticmethod
    def clone(name: str, val):
        return FloatValue(name, val)

    def copy(self):
        return FloatValue(self._name, self._data, unit=self.unit, v_max=self.max, v_min=self.min)

    @staticmethod
    def parse(s: str):
        try:
            v = float(s)
            return IntegerValue('Float', v)
        except ValueError:
            return None


class StringValue(BaseValue):
    def __init__(self, name: str, data: str=''):
        BaseValue.__init__(self, name, StringType(), data)

    def set_data(self, data):
        self._data = str(data)

    @staticmethod
    def clone(name: str, val):
        return StringValue(name, val)

    def copy(self):
        return StringValue(self._name, self.data())

    def __add__(self, other):
        if self.compatible(other):
            return self.clone(self._name + '+' + other.name(), self.data() + other.data())

    def __str__(self):
        return str(self._data)

    @staticmethod
    def parse(s: str):
        return StringValue('Str', s)