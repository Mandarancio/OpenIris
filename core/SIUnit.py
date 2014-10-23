__author__ = 'martino'
import math
from fractions import gcd


def m_gcd(l: list):
    """
    found the gcd of multiple values
    :param l: list of values
    :return: gcd
    """
    if len(l) == 1:
        return l[0]
    elif len(l) <= 0:
        return 0
    else:
        a = l[0]
        for i in range(1, len(l)):
            a = gcd(a, l[i])
        return a


class Unit:
    def __init__(self, name, sym, magnitude: int=1, base: int=0):
        self._name = name
        self._symbol = sym
        self._magnitude = magnitude
        self._base = base
        if magnitude == 0:
            self._name = ''
            self._symbol = ''

    def name(self):
        return self._name

    def complex(self):
        return False

    def symbol(self):
        return self._symbol

    def set_magnitude(self, val: int):
        self._magnitude = val

    def magnitude(self):
        return self._magnitude

    def print(self, val):
        if isinstance(val, float) or isinstance(val,int):
            if math.fabs(val) > 1:
                base = math.floor(math.log10(float(math.fabs(val))))
            else:
                base = 0
            v = float(val) / math.pow(10, base)
            return str(v) + self.to_str(int(base))
        else:
            return str(val) + str(self)

    def to_str(self, base: int):
        v = base + self._base
        if v >= 12:
            s = ('E' + str(v - 12) if v != 12 else '') + ' T'
        elif v >= 9:
            s = ('E' + str(v - 9) if v != 9 else '') + ' G'
        elif v >= 6:
            s = ('E' + str(v - 6) if v != 6 else '') + ' M'
        elif v >= 3:
            s = ('E' + str(v - 3) if v != 3 else '') + ' k'
        elif v >= 0:
            s = ('E' + str(v - 0) if v != 0 else '') + ' '
        elif v >= -3:
            s = ('E' + str(v + 3) if v != -3 else '') + ' m'
        elif v >= -6:
            s = ('E' + str(v + 6) if v != -6 else '') + ' μ'
        elif v >= -9:
            s = ('E' + str(v + 9) if v != -9 else '') + ' n'
        else:
            s = ('E' + str(v + 12) if v != -12 else '') + ' p'
        return s + str(self)

    def _base_to_str(self):
        if self._base >= 12:
            s = 'T'
        elif self._base >= 9:
            s = 'G'
        elif self._base >= 6:
            s = 'M'
        elif self._base >= 3:
            s = 'K'
        elif self._base >= 0:
            s = ''
        elif self._base >= -3:
            s = 'm'
        elif self._base >= -6:
            s = 'μ'
        elif self._base >= -9:
            s = 'n'
        else:
            s = 'p'
        return s + self._symbol

    def base(self):
        return self._base

    def inv(self):
        return Unit(self._name, self._symbol, -self._magnitude, self._base)

    def __mul__(self, other):
        if other.name() == self._name:
            return Unit(self._name, self._symbol, self._magnitude + other.magnitude(), self._base)
        else:
            return UnitManager.compose([self, other])

    def __truediv__(self, other):
        if other.name() == self._name:
            return Unit(self._name, self._symbol, self._magnitude - other.magnitude(), self._base)
        else:
            return UnitManager.compose([self, other.inv()])

    def __str__(self):
        if self._symbol == '':
            return ''
        return self._base_to_str() + (str(self._magnitude) if self._magnitude != 1 else '')


class NoUnit(Unit):
    def __init__(self):
        Unit.__init__(self, '', '', 0, 0)


class ComplexUnit(Unit):
    def __init__(self, name, sym, base_units: list, magnitude: int=1, base: int=0):
        Unit.__init__(self, name, sym, magnitude, base)
        self._base_units = base_units
        self.simplify()

    def complex(self):
        return True

    def inv(self):
        l = []
        for u in self._base_units:
            l.append(u.inv())
        return ComplexUnit(self._name, self._symbol, l, -self._magnitude, self._base)

    def simplify(self):
        l = {}
        for u in self._base_units:
            if u.name() in l:
                l[u.name()] *= u
            else:
                l[u.name()] = u
        ln = []
        for k in l:
            ln.append(abs(l[k].magnitude()))
        self._magnitude = m_gcd(ln)
        if self._magnitude < 1:
            self._magnitude = 1
        self._base_units.clear()
        for k in l:
            l[k].set_magnitude(l[k].magnitude() // self._magnitude)
            self._base_units.append(l[k])

    def base_units(self):
        return self._base_units

    def __mul__(self, other):
        if other.name() == self._name:
            return ComplexUnit(self._name, self._symbol, self._base_units, self._magnitude + other.magnitude(),
                               self._base)
        else:
            return UnitManager.compose([self, other])

    def __truediv__(self, other):
        if other.name() == self._name:
            return ComplexUnit(self._name, self._symbol, self._base_units, self._magnitude - other.magnitude(),
                               self._base)
        else:
            return UnitManager.compose([self, other.inv()])

    def __str__(self):
        if len(self._symbol) > 0:
            return self._symbol + (str(self._magnitude) if self._magnitude != 1 else '')
        else:
            s = ''
            if self._magnitude != 1:
                s = '('
            for u in self._base_units:
                s += str(u)
            if self._magnitude != 1:
                s += ')' + str(self._magnitude)
            return s


class Metre(Unit):
    def __init__(self, magnitude: int=1):
        Unit.__init__(self, 'Metre', 'm', magnitude, 0)


class Second(Unit):
    def __init__(self, magnitude: int=1):
        Unit.__init__(self, 'Second', 's', magnitude, 0)


class Kelvin(Unit):
    def __init__(self, magnitude: int=1):
        Unit.__init__(self, 'Kelvin', 'K', magnitude, 0)


class Celsius(Unit):
    def __init__(self, magnitude: int=1):
        Unit.__init__(self, 'Celsius', 'C', magnitude, 0)


class Candela(Unit):
    def __init__(self, magnitude: int=1):
        Unit.__init__(self, 'Candela', 'cd', magnitude, 0)


class KiloGram(Unit):
    def __init__(self, magnitude: int=1):
        Unit.__init__(self, 'Kilogram', 'g', magnitude, 3)


class Mole(Unit):
    def __init__(self, magnitude: int=1):
        Unit.__init__(self, 'Mole', 'mol', magnitude, 0)


class Ampere(Unit):
    def __init__(self, magnitude: int=1):
        Unit.__init__(self, 'Ampere', 'A', magnitude, 0)


class Hertz(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Hertz', 'Hz', [Second(-1)], magnitude, 0)


class Newton(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Newton', 'N', [KiloGram(), Metre(), Second(-2)], magnitude, 0)


class Pascal(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Pascal', 'Pa', [KiloGram(), Metre(-1), Second(-2)], magnitude, 0)


class Joule(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Joule', 'J', [KiloGram(), Metre(2), Second(-2)], magnitude, 0)


class Watt(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Watt', 'W', [KiloGram(), Metre(2), Second(-3)], magnitude, 0)


class Coulomb(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Coulomb', 'C', [Ampere(), Second()], magnitude, 0)


class Volt(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Volt', 'V', [KiloGram(), Metre(2), Second(-3), Ampere(-1)], magnitude, 0)


class Farad(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Farad', 'F', [KiloGram(-1), Metre(-2), Second(4), Ampere(2)], magnitude, 0)


class Ohm(ComplexUnit):
    def __init__(self, magnitude: int=1):
        ComplexUnit.__init__(self, 'Ohm', 'Ω', [KiloGram(), Metre(2), Second(-3), Ampere(-2)], magnitude, 0)


class UnitManager:
    base_si_units = [Metre(), Second(), KiloGram(), Kelvin(), Mole(), Candela(), Ampere()]
    complex_si_units = [Newton(), Joule(), Pascal(), Watt(), Coulomb(), Volt(), Ohm(), Farad()]

    @staticmethod
    def compose(units):
        l = []
        for u in units:
            if u.complex():
                l.extend(u.base_units())
            else:
                l.append(u)
        c = ComplexUnit('', '', l, 1, 0)
        res = UnitManager.match(c)
        if len(res) == 1:
            return res[0]
        else:
            return ComplexUnit('', '', res, 1, 0)

    @staticmethod
    def match(u: ComplexUnit):
        rest = u.base_units()
        best = u
        degree = 0
        for bu in rest:
            degree += abs(bu.magnitude())
        for cu in UnitManager.complex_si_units:
            r1 = UnitManager.diff(cu, u)
            if len(r1) <= len(rest):
                d = 0
                for bu in r1:
                    d += abs(bu.magnitude())
                if d < degree:
                    best = cu
                    rest = r1
        bests = [best]
        if len(rest) != len(u.base_units()):
            if len(rest) > 0:
                rest = UnitManager.match(ComplexUnit('', '', rest))
                bests.extend(rest)
        return bests

    @staticmethod
    def diff(c1: Unit, c2: Unit):
        l1 = []
        l2 = []
        rest = []
        if issubclass(c1.__class__, ComplexUnit):
            l1.extend(c1.base_units())
        else:
            l1.append(c1)

        if issubclass(c2.__class__, ComplexUnit):
            l2.extend(c2.base_units())
        else:
            l2.append(c2)
        for u in l1:
            ind = UnitManager.find(u, l2)
            if ind >= 0:
                if u.magnitude() != l2[ind].magnitude():
                    rest.append(l2[ind] / u)
            else:
                rest.append(u.inv())

        for u in l2:
            if UnitManager.find(u, l1) < 0:
                rest.append(u)

        return rest

    @staticmethod
    def find(u: Unit, l: list):
        for i in range(0, len(l)):
            if l[i].name() == u.name():
                return i
        return -1