from __future__ import annotations

import numbers
from io import UnsupportedOperation


class Time:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}s'

    def __add__(self, other):
        if isinstance(other, Time):
            return Time(self.value + other.value)
        else:
            raise UnsupportedOperation('+')

    def __mul__(self, other):
        if isinstance(other, Power):
            return Energy(self.value * other.value)
        else:
            raise UnsupportedOperation('*')

    @staticmethod
    def from_minutes(time: float) -> Time:
        return Time(time * 60 * 10)

    @staticmethod
    def from_hours(time: float) -> Time:
        return Time(time * 3600)

    def format_minutes(self):
        return f'{self.value / 60:.2f}min'

    def format_hours(self):
        return f'{self.value / 3600:.2f}h'


class Energy:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}J'

    def __add__(self, other):
        if isinstance(other, Energy):
            return Energy(self.value + other.value)
        else:
            raise UnsupportedOperation('+')

    def __sub__(self, other):
        if isinstance(other, Energy):
            return Energy(self.value - other.value)
        else:
            raise UnsupportedOperation('-')

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Energy(self.value * other)
        else:
            raise UnsupportedOperation('*')

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return Energy(self.value / other)
        else:
            raise UnsupportedOperation('/')

    def __rdiv__(self, other):
        raise UnsupportedOperation('/')

    def __lt__(self, other):
        if isinstance(other, Energy):
            return self.value < other.value
        else:
            raise UnsupportedOperation('<')

    @staticmethod
    def from_watt_seconds(energy: float) -> Energy:
        return Energy(energy)

    @staticmethod
    def from_watt_hours(energy: float) -> Energy:
        return Energy(energy * 3600)

    @staticmethod
    def from_kilo_watt_hours(energy: float) -> Energy:
        return Energy(energy * 3600 * 1000)

    def format_watt_seconds(self):
        return f'{self.value:.2f}Ws'

    def format_watt_hours(self):
        return f'{self.value / 3600:.2f}Wh'

    def format_kilo_watt_hours(self):
        return f'{self.value / 3600 / 1000:.2f}kWh'

    def format_watt_day(self):
        return f'{self.value * 24 * 3600:.2f}bob'


class Power:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}W'

    @staticmethod
    def from_kilo_watt(energy: float) -> Energy:
        return Energy(energy * 1000)

    def format_kilo_watt(self):
        return f'{self.value / 1000:.2f}kW'

    def __add__(self, other):
        if isinstance(other, Power):
            return Power(self.value + other.value)
        else:
            raise UnsupportedOperation('+')

    def __mul__(self, other):
        if isinstance(other, Time):
            return Energy(self.value * other.value)
        elif isinstance(other, numbers.Number):
            return Power(self.value * other)
        else:
            raise UnsupportedOperation('*')

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return Power(self.value / other)
        else:
            raise UnsupportedOperation('/')

    def __rdiv__(self, other):
        raise UnsupportedOperation('/')


class Temperature:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}K'

    def __add__(self, other):
        if isinstance(other, Temperature):
            return Temperature(self.value + other.value)
        else:
            raise UnsupportedOperation('+')

    def __sub__(self, other):
        if isinstance(other, Temperature):
            return Temperature(self.value - other.value)
        else:
            raise UnsupportedOperation('-')

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Temperature(self.value * other)
        else:
            raise UnsupportedOperation('*')

    def __truediv__(self, other):
        if isinstance(other, Temperature):
            return Temperature(self.value / other.value)
        else:
            raise UnsupportedOperation('/')

    def __lt__(self, other):
        if isinstance(other, Temperature):
            return self.value < other.value

    def __rdiv__(self, other):
        raise UnsupportedOperation('/')

    @staticmethod
    def from_celsius(temperature: float) -> Temperature:
        return Temperature(temperature + 273.15)

    @staticmethod
    def from_fahrenheit(temperature: float) -> Temperature:
        return Temperature((temperature - 459.67) * (5 / 9))

    def format_celsius(self):
        return f'{self.value - 273.15:.2f}°C'

    def format_fahrenheit(self):
        return f'{self.value * (9 / 5) - 459.67:.2f}°F'

    @staticmethod
    def get_specific_heat_capacity(energy: Energy, specific_heat_capacity: float, weight: float) -> Temperature:
        """
        Calculates the specific heat capacity.

        :param energy: in Joule, transforms itself into kJ
        :param specific_heat_capacity:
        :param weight: in kg
        :return:
        """
        return Temperature(((energy / 1000) / (specific_heat_capacity * weight)).value)


class Money:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}€'

    def __add__(self, other):
        if isinstance(other, Money):
            return Money(self.value + other.value)
        else:
            raise UnsupportedOperation('+')

    def __sub__(self, other):
        if isinstance(other, Money):
            return Money(self.value - other.value)
        else:
            raise UnsupportedOperation('-')

    def __mul__(self, other) -> Money:
        if isinstance(other, numbers.Number):
            return Money(self.value * other)
        elif isinstance(other, Energy):
            return Money(self.value * other.value)
        else:
            raise UnsupportedOperation('*')

    def __truediv__(self, other) -> Money:
        if isinstance(other, numbers.Number):
            return Money(self.value / other)
        else:
            raise UnsupportedOperation('/')

    def __rdiv__(self, other):
        raise UnsupportedOperation('/')
