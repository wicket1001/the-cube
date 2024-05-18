import numbers

from DebugLevel import DebugLevel
from Physics import Energy, Length, Density, SpecificHeatCapacity, Temperature


class SandBattery:
    capacity = Energy.from_kilo_watt_hours(25000)
    length = Length(0)
    width = Length(0)
    height = Length(0)
    density = Density.from_predefined(Density.Predefined.SAND)
    efficiency = 1
    shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.SAND)
    LOSS_PER_HOUR = 0.01
    LOSS_PER_STEP = LOSS_PER_HOUR / 6

    def __init__(self,
                 length: [numbers.Number, Length],
                 width: [numbers.Number, Length],
                 height: [numbers.Number, Length]):
        if isinstance(length, numbers.Number):
            self.length = Length(float(length))
        elif isinstance(length, Length):
            self.length = length
        else:
            raise NotImplementedError('length')

        if isinstance(width, numbers.Number):
            self.width = Length(float(width))
        elif isinstance(width, Length):
            self.width = width
        else:
            raise NotImplementedError('width')

        if isinstance(height, numbers.Number):
            self.height = Length(float(height))
        elif isinstance(height, Length):
            self.height = height
        else:
            raise NotImplementedError('height')

        volume = self.width * self.height * self.length
        mass = self.density.calculate_mass(volume)
        self.capacity = self.shc.calculate_energy((Temperature.from_celsius(500) - Temperature.from_celsius(20)), mass)

        self.battery_level = Energy(0)
        self.stored = Energy(0)
        self.taken = Energy(0)

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL):
        self.stored = self.stored * (1 - self.LOSS_PER_STEP)
