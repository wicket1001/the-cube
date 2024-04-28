from Appliance import Appliance
from Physics import Power, Time, Energy


class Fridge(Appliance):
    # https://www.co2online.de/energie-sparen/strom-sparen/strom-sparen-stromspartipps/kuehlschrank/
    # A+++: 95-125kWh
    # 2002: 330kWh

    WATTS = Power(150)
    SPLITTER = 8
    name = 'Fridge'

    def __init__(self):
        super().__init__()

    def step(self, t: int) -> Energy:
        energy_demand = Energy(0)
        self.on = False
        if t % self.SPLITTER * 4 < self.SPLITTER:
            self.on = True
            energy_demand = self.get_energy_demand()
        self.usage += energy_demand
        return energy_demand

    def get_energy_demand(self) -> Energy:
        # https://reductionrevolution.com.au/blogs/how-to/fridge-power-consumption
        return self.WATTS * Time.from_minutes(10)
