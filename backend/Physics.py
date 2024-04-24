from __future__ import annotations

from enum import IntFlag, auto
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
    def from_kilo_joule(energy: float) -> Energy:
        return Energy(energy * 1000)

    @staticmethod
    def from_watt_seconds(energy: float) -> Energy:
        return Energy(energy)

    @staticmethod
    def from_watt_hours(energy: float) -> Energy:
        return Energy(energy * 3600)

    @staticmethod
    def from_kilo_watt_hours(energy: float) -> Energy:
        return Energy(energy * 3600 * 1000)

    def format_kilo_joule(self):
        return f'{self.value / 1000:.2f}kJ'

    def format_watt_seconds(self):
        return f'{self.value:.2f}Ws'

    def format_watt_hours(self):
        return f'{self.value / 3600:.2f}Wh'

    def format_kilo_watt_hours(self):
        return f'{self.value / 3600 / 1000:.2f}kWh'

    def format_watt_day(self):
        return f'{self.value / 3600 / 24:.2f}Wd'

    def format_kilo_watt_day(self):
        return f'{self.value / 3600 / 1000 / 24:.2f}kWd'


class Power:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}W'

    @staticmethod
    def from_kilo_watt(energy: float) -> Power:
        return Power(energy * 1000)

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


class Weight:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}g'

    @staticmethod
    def from_kilo_gramm(value: float) -> Weight:
        return Weight(value * 1000)

    def format_kilo_gramm(self):
        return f'{self.value / 1000:.2f}kg'


class Length:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}m'

    def __add__(self, other):
        if isinstance(other, Length):
            return Length(self.value + other.value)
        else:
            raise UnsupportedOperation('*')

    def __mul__(self, other):
        if isinstance(other, Length):
            return Length(self.value * other.value)
        elif isinstance(other, numbers.Number):
            return Length(self.value * other)
        else:
            raise UnsupportedOperation('*')

    def format_square_metres(self):
        return f'{self.value:.2f}m^2'

    def format_qubic_metres(self):
        return f'{self.value:.2f}m^3'


class Density:
    value = 0

    # https://de.wikipedia.org/wiki/Dichte
    __density = {
        'air': 1.293,
        'wood': 200,  # 200-1200
        'water': 1000,
        'iron': 7874,
        'concrete': 2400
    }

    class Predefined(IntFlag):
        AIR = auto()
        WOOD = auto()
        WATER = auto()
        IRON = auto()
        CONCRETE = auto()

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}ρ'

    @staticmethod
    def from_predefined(material: Predefined) -> Density:
        return Density(Density.__density[
                           material.name.lower().replace('_', ' ')
                       ])

    @staticmethod
    def from_name(name: str) -> Density:
        return Density(Density.__density[name.lower()])

    def calculate_mass(self, volume: Length) -> Weight:
        return Weight.from_kilo_gramm(self.value * volume.value)

    def calculate_volume(self, mass: Weight) -> Length:
        return Length(mass.value / self.value / 1000)


class SpecificHeatCapacity:
    value = 0

    # https://de.wikipedia.org/wiki/Spezifische_W%C3%A4rmekapazit%C3%A4t
    # c [kJ/(kg*K)]
    __specific_heat_capacity = {
        'wood': 1.7,
        'plaster': 1.09,
        'glass': 0.67,  # 0.67-0.84
        'iron': 0.452,  # iron, cast iron 0.452-0.55
        'water': 4.18,
        'glycerine': 2.43,
        'steam': 2.08,  # (100°C)
        'air': 1.01,  # (dry)
        'wood fiber insulation': 2.1,  # cellulose flakes
        'polystyrene': 1.4,
        'concrete': 0.88
    }

    class Predefined(IntFlag):
        WOOD = auto()
        PLASTER = auto()
        GLASS = auto()
        IRON = auto()
        WATER = auto()
        GLYCERINE = auto()
        STEAM = auto()
        AIR = auto()
        WOOD_FIBER_INSULATION = auto()
        POLYSTYRENE = auto()
        CONCRETE = auto()

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}c'  # [kJ/(kg*K)]

    @staticmethod
    def from_predefined(material: Predefined) -> SpecificHeatCapacity:
        return SpecificHeatCapacity(
            SpecificHeatCapacity.__specific_heat_capacity[
                material.name.lower().replace('_', ' ')
            ]
        )

    @staticmethod
    def from_name(name: str) -> SpecificHeatCapacity:
        return SpecificHeatCapacity(
            SpecificHeatCapacity.__specific_heat_capacity[name.lower()]
        )

    def calculate_energy(self, temperature: Temperature, mass: Weight) -> Energy:
        """
        Calculates the needed energy for a given temperature delta.

        :param temperature:
        :param mass:
        :return:
        """
        return Energy(self.value * (mass.value / 1000) * temperature.value * 1000)

    def calculate_heat(self, energy: Energy, mass: Weight) -> Temperature:
        """
        Calculates the generated heat from the given energy.

        :param energy:
        :param mass:
        :return:
        """
        return Temperature((energy.value / 1000) / (self.value * (mass.value / 1000)))


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
        else:
            raise UnsupportedOperation('*')

    def __truediv__(self, other) -> Money:
        if isinstance(other, numbers.Number):
            return Money(self.value / other)
        else:
            raise UnsupportedOperation('/')

    def __rdiv__(self, other):
        raise UnsupportedOperation('/')

    @staticmethod
    def from_cent(value) -> Money:
        return Money(value / 100)

    def calculate_kWh_cost(self, energy: Energy) -> Money:
        return Money(self.value * (energy.value / 3600) / 1000)
