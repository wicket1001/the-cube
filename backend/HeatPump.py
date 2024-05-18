from DebugLevel import DebugLevel
from Appliance import Appliance
from Physics import Length, Energy, Power, Time, SpecificHeatCapacity, Density, Temperature, Weight


class HeatPump(Appliance):
    # https://en.wikipedia.org/wiki/Coefficient_of_performance
    name = 'HeatPump'

    COP = 3
    INITIAL_TEMPERATURE_C = 0
    water_weight = Weight(0)
    water_temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    water_density = Density.from_predefined(Density.Predefined.WATER)
    water_shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.WATER)

    should_activate = False

    def __init__(self, watts: float):
        super().__init__(watts)

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL):
        if self.water_weight.value == 0:
            raise AttributeError('Water heated cannot be 0l.')
        if self.should_activate:
            energy_demand = self.get_energy_demand()
            self.usage += energy_demand
            self.generate_heat(energy_demand, verbosity)
            return energy_demand
        else:
            return Energy(0)

    def input_water(self, litre: Length, temperature: Temperature) -> None:
        self.water_weight = self.water_density.calculate_mass(litre)
        self.water_temperature = temperature

    def output_water(self) -> (Weight, Temperature):
        temp = Weight(self.water_weight.value), Temperature(self.water_temperature.value)
        self.water_weight = Weight(0)
        self.water_temperature = Temperature.from_celsius(self.INITIAL_TEMPERATURE_C)
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
        if self.water_weight.value == 0:
            raise AttributeError('Water heated cannot be 0l.')
        if verbosity >= DebugLevel.DEBUGGING:
            print(self.water_temperature.value, energy)
        initial_temperature = Temperature(self.water_temperature.value)
        water_energy = self.water_shc.calculate_energy(self.water_temperature, self.water_weight)
        if verbosity >= DebugLevel.DEBUGGING:
            print(water_energy)
        water_energy += energy * self.COP
        if verbosity >= DebugLevel.DEBUGGING:
            print(water_energy)
        self.water_temperature = self.water_shc.calculate_heat(water_energy, self.water_weight)
        return self.water_temperature - initial_temperature

    def calculate_energy(self, temperature: Temperature, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        if self.water_weight.value == 0:
            raise AttributeError('Water heated cannot be 0l.')
        initial_energy = self.water_shc.calculate_energy(self.water_temperature, self.water_weight)
        output_water_t = self.water_temperature + temperature
        output_energy = self.water_shc.calculate_energy(output_water_t, self.water_weight)
        input_energy = (output_energy - initial_energy) / 3
        return input_energy

    def get_energy_demand(self) -> Energy:
        return self.WATTS * Time.from_minutes(10)

    def activate(self):
        self.should_activate = True

    def deactivate(self):
        self.should_activate = False
