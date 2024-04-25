from Physics import Power, Energy


class Appliance:
    name = ''
    WATTS = Power(0)
    usage = Energy(0)

    def __init__(self):
        pass

    def __str__(self):
        return f'Appliance used {self.usage}'

    def step(self, t: int) -> Energy:
        return Energy(0)

    def print_statistics(self):
        print(f'{self.name} used: {self.usage.format_kilo_watt_hours()}')
