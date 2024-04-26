import math
import numbers
from typing import List

from Physics import *
from Generator import Generator


class Windturbine(Generator):
    EFFICIENCY = 0.8
    RHO = 1.295

    generation = Energy(0)
    winds = []
    area = Length(1)
    name = 'Windturbine'

    def __init__(self, size: [numbers.Number, Length], angle: numbers.Number):
        super().__init__(size)
        self.angle = angle

    def save_weather(self, array: List[float], array2: List[float]):
        self.winds = array
        self.wind_directions = array2

    def step(self, t: int, absolute_step: int) -> Energy:
        wind = self.winds[absolute_step]
        print(f'v={wind}')
        relative_angle = float(self.angle) + self.wind_directions[absolute_step]
        print(f'relative_angle={relative_angle}')
        foo = math.cos(relative_angle * math.pi / 180)
        print(f'foo={foo}')
        direction_loss = abs(foo)
        print(f'direction_loss={direction_loss}')
        watt = Power(0.5 * self.RHO * self.area.value * (wind ** 3))
        print(f'watt={watt}')
        effective_watt = Power(watt.value * direction_loss)
        print(f'effective_watt={effective_watt}')
        energy = effective_watt * Time.from_minutes(10)
        print(f'energy={energy}')
        print(f'energy={energy.format_watt_hours()}')
        self.generation += energy
        return energy

    def print_statistics(self):
        print(f'{self.name} Produced: {self.generation.format_kilo_watt_hours()}')
        print(f'{self.name} Produced: {self.generation.format_watt_hours()}')
        print(f'--')
