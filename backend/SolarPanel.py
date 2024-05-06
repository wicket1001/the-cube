import math
import numbers
from typing import List

from DebugLevel import DebugLevel
from Physics import Energy, Power, Time, Length
from Generator import Generator


class SolarPanel(Generator):
    # 52MW
    # 26/15 MW pro Tag
    # 576m^2 Solarpanel
    # 0.003009 MW pro Panel pro Tag
    # 3009 W pro Panel pro Tag
    EFFICIENCY = 0.2
    # JOULE_TO_KWH = 0.000000278

    watt_sum = Power(0)
    solar_energy = Energy(0)
    iterations = 0
    radiations = []

    name = 'SolarPanel'

    def __init__(self, size: [numbers.Number, Length]):
        super().__init__(size)

    def save_weather(self, array: List[float]):
        self.radiations = array

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        self.iterations += 1
        if len(self.radiations) == 0:
            # return int(math.sin(t) * 1000)
            energy_production = Energy(math.sin(t / (144/math.pi)) * 100)
            energy_production *= self.area.value
            self.generation += energy_production
            return energy_production
        else:
            # print(absolute_step)
            energy_production = 0
            radiation = self.radiations[absolute_step]
            # print('Rad', radiation)

            watt = Power(radiation * self.area.value)
            # print('WATT', watt)
            joule_per_10min = watt * Time.from_minutes(10)
            # print('Joule', joule_per_10min)

            factor = math.sin(t / (144/3))
            # print('Time factor', factor)
            effective_watt = watt * factor
            effective_joule = joule_per_10min * factor
            # print('Effective Joule', effective_joule)

            self.solar_energy += joule_per_10min
            energy_production = joule_per_10min * self.EFFICIENCY  # * (1/3600)
            # energy_production = joule_per_10min * self.solar_panel_efficiency # TODO effective_joule
            # print('Energy production', energy_production)

            self.watt_sum += watt
            self.generation += energy_production
            return energy_production

    def print_statistics(self):
        print(f'{self.name} Produced: {self.generation.format_kilo_watt_hours()}')
        if self.iterations == 144:
            avg_watt = self.watt_sum / 144
            print(f'Watt Average: {avg_watt}')
            watt_second = (avg_watt * self.EFFICIENCY) / Time.from_hours(1)
            print(f'Watt / seconds: {watt_second}')
            watt_per_day = watt_second * Time.from_hours(24).value
            print(f'watt_per_day: {watt_per_day}')
            print(f'watt_per_day: {watt_per_day.format_kilo_watt()}')
