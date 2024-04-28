from Appliance import Appliance
from DebugLevel import DebugLevel
from Physics import Power, Time, Energy


class Lights(Appliance):
    WATTS = Power(25)
    name = 'Lights'

    def __init__(self):
        super().__init__()

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel) -> Energy:
        self.on = True
        energy_demand = self.get_energy_demand()
        self.usage += energy_demand
        return energy_demand

    def get_energy_demand(self) -> Energy:
        # https://www.beleuchtungdirekt.at/lumen-nach-watt
        # Glühbirne: 25-30Watt
        # Energiesparlampe: 5-6Watt
        # LED: 2-4Watt

        # 1Watt -> 24Wh
        return self.WATTS * Time.from_minutes(10)
