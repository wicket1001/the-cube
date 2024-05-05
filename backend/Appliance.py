from DebugLevel import DebugLevel
from Physics import Power, Energy


class Appliance:
    name = ''
    WATTS = Power(0)
    usage = Energy(0)
    on = False

    def __init__(self, watts: float):
        self.WATTS = Power(watts)

    def __str__(self):
        return f'Appliance used {self.usage}'

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel) -> Energy:
        return Energy(0)

    def print_statistics(self):
        print(f'{self.name} used: {self.usage.format_kilo_watt_hours()}')
