import numbers
from typing import List

from DebugLevel import DebugLevel
from Generator import Generator
from Physics import Length, Energy, Power, Time, SpecificHeatCapacity, Density, Temperature, Weight


class SolarThermal(Generator):
    EFFICIENCY = 0.2
    WATER_EFFICIENCY = 0.85

    iterations = 0

    INITIAL_TEMPERATURE_C = 0
    solar_energy = Energy(0)
    radiations = []
    water_weight = Weight(0)
    water_temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    water_density = Density.from_predefined(Density.Predefined.WATER)
    water_shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.WATER)

    name = "SolarThermal"

    def __init__(self, size: [numbers.Number, Length]):
        super().__init__(size)

    def save_weather(self, array: List[float]):
        self.radiations = array

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        self.iterations += 1
        radiation = self.radiations[absolute_step]
        watt = Power(radiation * self.area.value)
        joule = watt * Time.from_minutes(10)
        self.solar_energy += joule
        energy_production = joule * self.EFFICIENCY

        heat_production = joule * self.WATER_EFFICIENCY
        self.water_temperature += self.water_shc.calculate_heat(heat_production, self.water_weight)
        print(self.water_temperature.format_celsius())

        self.generation += energy_production
        return energy_production

    def input_water(self, litre: Length, temperature: Temperature):
        self.water_weight = self.water_density.calculate_mass(litre)
        self.water_temperature = temperature

    def output_water(self) -> (Weight, Temperature):
        temp = Weight(self.water_weight.value), Temperature(self.water_temperature.value)
        self.water_weight = Weight(0)
        self.water_temperature = Temperature.from_celsius(self.INITIAL_TEMPERATURE_C)
        return temp

    def print_statistics(self):
        print(f'{self.name} produced: {self.generation.format_watt_hours()}')
