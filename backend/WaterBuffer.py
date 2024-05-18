from DebugLevel import DebugLevel
from Physics import Weight, Temperature, Density, SpecificHeatCapacity, Length, Energy


class WaterBuffer:
    name = 'WaterBuffer'
    INITIAL_TEMPERATURE_C = 0
    weight = Weight(0)
    temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    density = Density.from_predefined(Density.Predefined.WATER)
    shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.WATER)
    AMBIENT_TEMPERATURE_C = 7
    ambient_temperature = Temperature.from_celsius(AMBIENT_TEMPERATURE_C)
    LOSS_PER_HOUR = 0.01
    LOSS_PER_STEP = LOSS_PER_HOUR / 6

    def __init__(self, litre: Length, temperature: Temperature):
        self.weight = self.density.calculate_mass(litre)
        self.temperature = temperature

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        delta_t = self.temperature - self.ambient_temperature
        temperature_lost = Temperature(delta_t.value * self.LOSS_PER_STEP)
        energy_lost = self.shc.calculate_energy(temperature_lost, self.weight)
        if verbosity >= DebugLevel.DEBUGGING:
            print(energy_lost.format_watt_hours())
        self.temperature -= temperature_lost
        return energy_lost

    def add_water(self, litre: Length, temperature: Temperature) -> None:
        additional_water = self.density.calculate_mass(litre)
        additional_energy = self.shc.calculate_energy(temperature, additional_water)
        own_energy = self.shc.calculate_energy(self.temperature, self.weight)
        self.weight += additional_water
        self.temperature = self.shc.calculate_heat(own_energy + additional_energy, self.weight)

    def take_water(self, litre: Length) -> (Weight, Temperature):
        taken = self.density.calculate_mass(litre)
        self.weight -= taken
        if self.weight.value <= 0:
            raise AttributeError('Water cannot be taken that is not inside the water buffer.')
        return taken, Temperature(self.temperature.value)
