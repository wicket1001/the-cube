import numbers

from DebugLevel import DebugLevel
from Physics import Energy, Length, Density, SpecificHeatCapacity, Temperature, Weight


class SandBattery:
    name = 'SandBattery'

    INITIAL_TEMPERATURE_C = 0
    weight = Weight(0)
    temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    AMBIENT_TEMPERATURE_C = 0
    ambient_temperature = Temperature.from_celsius(AMBIENT_TEMPERATURE_C)

    capacity = Energy.from_kilo_watt_hours(11_000)
    length = Length(0)
    width = Length(0)
    height = Length(0)
    density = Density.from_predefined(Density.Predefined.SAND)
    efficiency = 1
    shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.SAND)
    LOSS_PER_DAY = 0.005
    LOSS_PER_HOUR = LOSS_PER_DAY / 24
    LOSS_PER_STEP = LOSS_PER_HOUR / 6

    COP = 1

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
        self.weight = self.density.calculate_mass(volume)
        # print(self.capacity.format_kilo_watt_hours())
        # self.capacity = self.shc.calculate_energy(
        #     (Temperature.from_celsius(500) - Temperature.from_celsius(20)),
        #     self.mass
        # )
        # print(self.capacity.format_kilo_watt_hours())

        self.battery_level = Energy(0)
        self.stored = Energy(0)
        self.taken = Energy(0)

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        delta_t = self.temperature - self.ambient_temperature
        temperature_lost = Temperature(delta_t.value * self.LOSS_PER_STEP)
        # self.stored = self.stored * (1 - self.LOSS_PER_STEP)
        energy_lost = self.shc.calculate_energy(temperature_lost, self.weight)
        if verbosity >= DebugLevel.DEBUGGING:
            print(energy_lost.format_watt_hours())
        self.temperature -= temperature_lost
        return energy_lost

    def generate_heat(self, energy: Energy, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Temperature:
        if self.weight.value <= 0:
            raise AttributeError(f'{self.name} heated cannot be smaller than 0.')
        if verbosity >= DebugLevel.DEBUGGING:
            print(self.temperature.format_celsius(), energy)
        initial_temperature = Temperature(self.temperature.value)
        total_energy = self.shc.calculate_energy(self.temperature, self.weight)
        if verbosity >= DebugLevel.DEBUGGING:
            print(total_energy)
        total_energy += energy * self.COP
        if verbosity >= DebugLevel.DEBUGGING:
            print(total_energy)
        self.temperature = self.shc.calculate_heat(total_energy, self.weight)
        return self.temperature - initial_temperature
