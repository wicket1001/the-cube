from Physics import Power, Energy


class Appliance:
    # 10min Timestamps means 6 measurements per hour
    TIMESTAMPS = 144
    TO_WATT_HOURS = 6
    HOURS = 24
    MINUTES = 60
    SPLITTER = 8
    WATTS = 0

    usage = Energy(0)

    def __init__(self):
        pass

    def __str__(self):
        return f'Appliance used {self.usage}'

    def step(self, t: int) -> Energy:
        return Energy(0)

    def print_statistics(self):
        print(f'Used: {self.usage}')
