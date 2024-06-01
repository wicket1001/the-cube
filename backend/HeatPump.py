from DebugLevel import DebugLevel
from Appliance import Appliance
from Physics import Length, Energy, Power, Time, SpecificHeatCapacity, Density, Temperature, Weight


class HeatPump(Appliance):
    # https://en.wikipedia.org/wiki/Coefficient_of_performance
    # https://heatpumps.co.uk/heat-pump-resources/numbers-and-calculations/
    name = 'HeatPump'

    COP = 3
    INITIAL_TEMPERATURE_C = 0
    weight = Weight(0)
    temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    water_density = Density.from_predefined(Density.Predefined.WATER)
    shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.WATER)

    should_activate = False

    flow_rate = Length.from_litre(0.015)

    def __init__(self, watts: float):
        super().__init__(watts)

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL):
        if self.weight.value == 0:
            raise AttributeError('Water heated cannot be 0l.')
        if self.should_activate:
            energy_demand = self.get_energy_demand()
            self.usage += energy_demand
            self.generate_heat(energy_demand, verbosity)
            return energy_demand
        else:
            return Energy(0)

    def input_water(self, litre: Length, temperature: Temperature) -> None:
        self.weight = self.water_density.calculate_mass(litre)
        self.temperature = temperature

    def output_water(self) -> (Weight, Temperature):
        temp = Weight(self.weight.value), Temperature(self.temperature.value)
        self.weight = Weight(0)
        self.temperature = Temperature.from_celsius(self.INITIAL_TEMPERATURE_C)
        return temp

    def generate_heat(self, energy: Energy, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Temperature:
        """
        Heats up the water with the given energy.
        The delta temperature that the water was heated up is returned.
        The water temperature is stored in self.water_temperature.

        :param energy: the energy applied to the water.
        :param verbosity: Verbosity level for debugging.
        :return: the delta temperature that the water was heated up
        """
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

    def calculate_energy(self, temperature: Temperature, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        if self.weight.value == 0:
            raise AttributeError('Water heated cannot be 0l.')
        initial_energy = self.shc.calculate_energy(self.temperature, self.weight)
        output_water_t = self.temperature + temperature
        output_energy = self.shc.calculate_energy(output_water_t, self.weight)
        input_energy = (output_energy - initial_energy) / self.COP
        return input_energy

    def get_energy_demand(self) -> Energy:
        return self.WATTS * Time.from_minutes(10)

    def activate(self):
        self.should_activate = True

    def deactivate(self):
        self.should_activate = False
