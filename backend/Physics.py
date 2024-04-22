from __future__ import annotations
import math


class Time(float):
    def __new__(cls, value):
        return float.__new__(cls, value)

    def __init__(self, value):
        float.__init__(value)

    def __str__(self):
        return f'{self:.2f}s'

    @staticmethod
    def from_hours(time: float) -> Time:
        return Time(time * 3600)


class Energy(float):
    def __new__(cls, value):
        return float.__new__(cls, value)

    def __init__(self, value):
        float.__init__(value)

    def __str__(self):
        return f'{self:.2f}J'

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
        return f'{self:.2f}Ws'

    def format_watt_hours(self):
        return f'{self / 3600:.2f}Wh'

    def format_kilo_watt_hours(self):
        return f'{self / 3600 / 1000:.2f}kWh'


class Power(float):
    def __new__(cls, value):
        return float.__new__(cls, value)

    def __init__(self, value):
        float.__init__(value)

    def __str__(self):
        return f'{self:.2f}W'

    @staticmethod
    def from_kilo_watt(energy: float) -> Energy:
        return Energy(energy * 1000)

    def format_kilo_watt(self):
        return f'{self / 1000:.2f}kW'

    def __mul__(self, other):
        if isinstance(other, Time):
            return Energy(self * float(other))


class Temperature(float):
    def __new__(cls, value):
        return float.__new__(cls, value)

    def __init__(self, value):
        float.__init__(value)

    def __str__(self):
        return f'{self:.2f}K'

    @staticmethod
    def from_celsius(temperature: float) -> Temperature:
        return Temperature(temperature + 273.15)

    @staticmethod
    def from_fahrenheit(temperature: float) -> Temperature:
        return Temperature((temperature - 459.67) * (5 / 9))

    def format_celsius(self):
        return f'{self - 273.15:.2f}°C'

    def format_fahrenheit(self):
        return f'{self * (9 / 5) - 459.67:.2f}°F'
