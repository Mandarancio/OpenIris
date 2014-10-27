__author__ = 'martino'
from core.UValue import *
import math


def u_pow(a: NumericalValue, b: NumericalValue):
    v = pow(a.data(), b.data())
    return FloatValue('Float', v)


def u_sqrt(a: NumericalValue):
    v = math.sqrt(a.data())
    return FloatValue('Float', v)


def u_sin(a: NumericalValue):
    v = math.sin(a.data())
    return FloatValue('Float', v)