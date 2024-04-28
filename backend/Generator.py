import math
import numbers
from typing import List

from DebugLevel import DebugLevel
from Physics import Energy, Power, Time, Length


class Generator:
    EFFICIENCY = 1

    generation = Energy(0)
    area = Length(1)
    name = 'Generator'

    def __init__(self, size: [numbers.Number, Length]):
        if isinstance(size, numbers.Number):
            self.area = Length(float(size))
        elif isinstance(size, Length):
            self.area = size
        else:
            raise NotImplementedError('size')

    def __str__(self):
        return self.name

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel) -> Energy:
        return Energy(0)

    def print_statistics(self):
        print(f'{self.name} produced: {self.generation.format_kilo_watt_hours()}')
