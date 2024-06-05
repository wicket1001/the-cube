from __future__ import annotations

from datetime import datetime
from enum import IntFlag, auto
import numbers
from io import UnsupportedOperation
from json import JSONEncoder


class SIEncoder(JSONEncoder):
    # https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)
        if (isinstance(o, Temperature)
                or isinstance(o, Time)
                or isinstance(o, Energy)
                or isinstance(o, Power)
                or isinstance(o, Weight)
                or isinstance(o, Length)
                or isinstance(o, Density)
                or isinstance(o, SpecificHeatCapacity)
                or isinstance(o, Money)):
            return o.value
        else:
            raise UnsupportedOperation(type(o))


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

    def __truediv__(self, other):
        if isinstance(other, Time):
            return self.value / other.value
        else:
            raise UnsupportedOperation('/')

    @staticmethod
    def from_minutes(time: float) -> Time:
        return Time(time * 60)

    @staticmethod
    def from_hours(time: float) -> Time:
        return Time(time * 3600)

    @staticmethod
    def from_days(time: float) -> Time:
        return Time(time * 3600 * 24)

    @staticmethod
    def from_years(time: float) -> Time:
        return Time(time * 3600 * 24 * 365)

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
        elif isinstance(other, Energy):
            return Energy(self.value / other.value)
        else:
            raise UnsupportedOperation('/')

    def __rdiv__(self, other):
        raise UnsupportedOperation('/')

    def __lt__(self, other):
        if isinstance(other, Energy):
            return self.value < other.value
        else:
            raise UnsupportedOperation('<')

    def __neg__(self):
        return Energy(-self.value)

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
        if isinstance(other, Time):
            return Power(self.value / other.value)
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

    def __abs__(self):
        return Temperature(abs(self.value))

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
        if isinstance(other, numbers.Number):
            return Temperature(self.value / float(other))
        else:
            raise UnsupportedOperation('/')

    def __lt__(self, other):
        if isinstance(other, Temperature):
            return self.value < other.value

    def __rdiv__(self, other):
        raise UnsupportedOperation('/')

    def get_celsius(self) -> float:
        return self.value - 273.15

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


class Weight:
    value = 0

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}g'

    def __add__(self, other):
        if isinstance(other, Weight):
            return Weight(self.value + other.value)
        else:
            raise UnsupportedOperation('+')

    def __sub__(self, other):
        if isinstance(other, Weight):
            return Weight(self.value - other.value)
        else:
            raise UnsupportedOperation('-')

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Weight(self.value * other)
        else:
            raise UnsupportedOperation('*')

    @staticmethod
    def from_kilo_gramm(value: float) -> Weight:
        return Weight(value * 1000)

    def format_kilo_gramm(self):
        return f'{self.value / 1000:.2f}kg'


class Length:
    value = 0

    # https://de.wikipedia.org/wiki/Angloamerikanisches_Ma%C3%9Fsystem

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value:.2f}m'

    def __add__(self, other):
        if isinstance(other, Length):
            return Length(self.value + other.value)
        else:
            raise UnsupportedOperation('+')

    def __sub__(self, other):
        if isinstance(other, Length):
            return Length(self.value - other.value)
        else:
            raise UnsupportedOperation('-')

    def __mul__(self, other):
        if isinstance(other, Length):
            return Length(self.value * other.value)
        elif isinstance(other, numbers.Number):
            return Length(self.value * other)
        else:
            raise UnsupportedOperation('*')

    def get_litres(self) -> float:
        return self.value * 1000.0

    @staticmethod
    def from_milli_meter(value: float) -> Length:
        return Length(value / 1000)

    @staticmethod
    def from_centi_meter(value: float) -> Length:
        return Length(value / 100)

    @staticmethod
    def from_kilo_meters(value: float) -> Length:
        return Length(value * 1000)

    @staticmethod
    def from_inch(value: float) -> Length:
        return Length(value * 0.0254)

    @staticmethod
    def from_foot(value: float) -> Length:
        return Length(value * 0.3048)

    @staticmethod
    def from_yard(value: float) -> Length:
        return Length(value * 0.9144)

    @staticmethod
    def from_mile(value: float) -> Length:
        return Length(value * 1609.344)

    @staticmethod
    def from_litre(litre: float) -> Length:
        return Length(litre / 1000.0)

    @staticmethod
    def from_milli_litre(milli_litre: float) -> Length:
        return Length(milli_litre / 1_000_000.0)

    @staticmethod
    def from_gallon(gallon: float) -> Length:
        return Length(gallon * 3.785411784 / 1000.0)

    def format_square_metres(self):
        return f'{self.value:.2f}m^2'

    def format_qubic_metres(self):
        return f'{self.value:.2f}m^3'

    def format_milli_metres(self):
        return f'{self.value * 1000:.2f}mm'

    def format_centi_metres(self):
        return f'{self.value * 100:.2f}cm'

    def format_kilo_metres(self):
        return f'{self.value / 1000:.2f}km'

    def format_inch(self):
        return f'{self.value / 0.0254:.2f}´´'

    def format_foot(self):
        return f'{self.value / 0.3048:.2f}´'

    def format_yard(self):
        return f'{self.value / 0.9144:.2f}yd'

    def format_mile(self):
        return f'{self.value / 1609.344:.2f}mi'

    def format_litre(self):
        return f'{self.value * 1000.0:.2f}l'

    def format_milli_litre(self):
        return f'{self.value * 1_000_000.0:.2f}ml'

    def format_gallon(self):
        return f'{self.value * 1000.0 / 3.785411784:.2f}gal'


class Density:
    value = 0

    # https://de.wikipedia.org/wiki/Dichte
    __density = {
        'air': 1.293,
        'wood': 200,  # 200-1200
        'water': 1000,
        'iron': 7874,
        'concrete': 2400,
        'sand': 1602,
        'co2': 1.98,
        'o2': 1.429
    }

    class Predefined(IntFlag):
        AIR = auto()
        WOOD = auto()
        WATER = auto()
        IRON = auto()
        CONCRETE = auto()
        SAND = auto()
        CO2 = auto()
        O2 = auto()

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
        'concrete': 0.88,
        'sand':0.83
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
        SAND = auto()

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
