from DebugLevel import DebugLevel
from Physics import Weight, Temperature, Density, SpecificHeatCapacity, Length, Energy


class WaterBuffer:
    name = 'WaterBuffer'
    INITIAL_TEMPERATURE_C = 0
    water_weight = Weight(0)
    water_temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    water_density = Density.from_predefined(Density.Predefined.WATER)
    water_shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.WATER)
    AMBIENT_TEMPERATURE_C = 7
    ambient_water_temperature = Temperature.from_celsius(AMBIENT_TEMPERATURE_C)
    LOSS_PER_HOUR = 0.01
    LOSS_PER_STEP = LOSS_PER_HOUR / 6

    def __init__(self, litre: Length, temperature: Temperature):
        self.water_weight = self.water_density.calculate_mass(litre)
        self.water_temperature = temperature

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        delta_t = self.water_temperature - self.ambient_water_temperature
        temperature_lost = Temperature(delta_t.value * self.LOSS_PER_STEP)
        energy_lost = self.water_shc.calculate_energy(temperature_lost, self.water_weight)
        if verbosity >= DebugLevel.DEBUGGING:
            print(energy_lost.format_watt_hours())
        self.water_temperature -= temperature_lost
        return energy_lost

    def add_water(self, litre: Length, temperature: Temperature) -> None:
        additional_water = self.water_density.calculate_mass(litre)
        additional_energy = self.water_shc.calculate_energy(temperature, additional_water)
        own_energy = self.water_shc.calculate_energy(self.water_temperature, self.water_weight)
        self.water_weight += additional_water
        self.water_temperature = self.water_shc.calculate_heat(own_energy + additional_energy, self.water_weight)

    def take_water(self, litre: Length) -> (Weight, Temperature):
        taken = self.water_density.calculate_mass(litre)
        self.water_weight -= taken
        if self.water_weight.value <= 0:
            raise AttributeError('Water cannot be taken that is not inside the water buffer.')
        return taken, Temperature(self.water_temperature.value)
