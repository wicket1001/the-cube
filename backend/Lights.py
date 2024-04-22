from Appliance import Appliance


class Lights(Appliance):
    WATTS = 25

    def __init__(self):
        super().__init__()

    def step(self, t: int):
        energy_demand = self.get_energy_demand()
        self.usage += energy_demand
        return energy_demand

    def get_energy_demand(self):
        # https://www.beleuchtungdirekt.at/lumen-nach-watt
        # Glühbirne: 25-30Watt
        # Energiesparlampe: 5-6Watt
        # LED: 2-4Watt

        # 1Watt -> 24Wh
        return self.WATTS / self.TO_WATT_HOURS
