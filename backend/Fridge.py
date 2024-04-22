from Appliance import Appliance


class Fridge(Appliance):
    WATTS = 150

    def __init__(self):
        super().__init__()

    def step(self, t: int):
        energy_demand = 0
        if t % self.SPLITTER * 2 < self.SPLITTER:
            energy_demand = self.get_energy_demand()
        self.usage += energy_demand
        return energy_demand

    def get_energy_demand(self):
        # https://reductionrevolution.com.au/blogs/how-to/fridge-power-consumption
        return self.WATTS / self.TO_WATT_HOURS
