from Appliance import Appliance
from Physics import Power, Time, Energy


class Fridge(Appliance):
    WATTS = Power(150)

    def __init__(self):
        super().__init__()

    def step(self, t: int) -> Energy:
        energy_demand = Power(0)
        if t % self.SPLITTER * 2 < self.SPLITTER:
            energy_demand = self.get_energy_demand()
        self.usage += energy_demand
        return energy_demand

    def get_energy_demand(self) -> Energy:
        # https://reductionrevolution.com.au/blogs/how-to/fridge-power-consumption
        return self.WATTS * Time.from_minutes(10)
