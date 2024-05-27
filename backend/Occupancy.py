from __future__ import annotations
from enum import IntFlag, auto

from Physics import Energy, Power, Time, Length, Weight, Density
from DebugLevel import DebugLevel

STEPS_PER_DAY = int((24 * 60) / 10)


class Occupancy:
    __occupancy = {
        'empty': 0,
        'low': 4,
        'medium': 10,
        'high': 15
    }

    class Predefined(IntFlag):
        EMPTY = auto()
        LOW = auto()
        MEDIUM = auto()
        HIGH = auto()

    name = 'Occupancy'
    density_co2 = Density.from_predefined(Density.Predefined.CO2)
    density_o2 = Density.from_predefined(Density.Predefined.O2)
    generated_heat = Energy(0)

    def __init__(self, occupants: int):
        self.taken_o2 = Weight(0)
        self.produced_co2 = Weight(0)
        self.taken_o2_litre = Length(0)
        self.produced_co2_litre = Length(0)

        self.occupants = occupants

        # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8672270/
        # https://pubs.asahq.org/anesthesiology/article/86/3/532/35822/How-Much-Oxygen-Does-the-Human-Lung-Consume
        self.litre_per_minute = Length.from_litre(5)
        self.o2_usage = self.litre_per_minute * 0.21 - self.litre_per_minute * 0.16
        self.co2_demand = self.litre_per_minute * 0.05 - self.litre_per_minute * 0.0004
        # print(self.o2_usage.format_milli_litre(),
        #       self.o2_usage.value,
        #       self.co2_demand.format_milli_litre(),
        #       self.co2_demand.value)

    @staticmethod
    def from_predefined(density: Predefined, quadratic_metres: Length) -> Occupancy:
        return Occupancy(int(Occupancy.__occupancy[
                            density.name.lower().replace('_', ' ')
                         ] * quadratic_metres.value / 10))

    def generate_heat(self, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:  # live
        energy = Power(100) * Time.from_minutes(10) * self.occupants
        if verbosity >= DebugLevel.DEBUGGING:
            print(energy.format_watt_hours())
        return energy

    def breath(self, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Length:
        co2 = self.co2_demand * 10 * self.occupants
        o2 = self.o2_usage * 10 * self.occupants

        if verbosity >= DebugLevel.DEBUGGING:
            print(o2.value, o2.format_milli_litre())
            print(co2.value, co2.format_milli_litre())
        mass_co2 = self.density_co2.calculate_mass(co2)
        mass_o2 = self.density_o2.calculate_mass(o2)
        if verbosity >= DebugLevel.DEBUGGING:
            print(mass_co2, mass_o2)

        self.taken_o2 += mass_o2
        self.produced_co2 += mass_co2
        self.taken_o2_litre += o2
        self.produced_co2_litre += co2

        return co2

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL):
        self.generate_heat(verbosity)
        self.breath(verbosity)
