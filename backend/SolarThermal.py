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
    weight = Weight(0)
    temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    density = Density.from_predefined(Density.Predefined.WATER)
    shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.WATER)

    name = "SolarThermal"

    def __init__(self, size: [numbers.Number, Length]):
        super().__init__(size)

    def save_weather(self, array: List[float]):
        self.radiations = array

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        if self.weight.value == 0:
            raise AttributeError('Water heated cannot be 0l.')
        self.iterations += 1
        radiation = self.radiations[absolute_step]
        watt = Power(radiation * self.area.value)
        joule = watt * Time.from_minutes(10)
        self.solar_energy += joule
        energy_production = joule * self.EFFICIENCY

        heat_production = joule * self.WATER_EFFICIENCY
        self.temperature += self.shc.calculate_heat(heat_production, self.weight)
        if verbosity >= DebugLevel.DEBUGGING:
            print(self.temperature.format_celsius())

        self.generation += energy_production
        return energy_production

    def input_water(self, litre: Length, temperature: Temperature) -> None:
        self.weight = self.density.calculate_mass(litre)
        self.temperature = temperature

    def output_water(self) -> (Weight, Temperature):
        temp = Weight(self.weight.value), Temperature(self.temperature.value)
        self.weight = Weight(0)
        self.temperature = Temperature.from_celsius(self.INITIAL_TEMPERATURE_C)
        return temp

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

    def print_statistics(self):
        print(f'{self.name} produced: {self.generation.format_watt_hours()}')
