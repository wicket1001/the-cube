from Appliance import Appliance
from DebugLevel import DebugLevel
from Physics import Power, Time, Energy, Temperature


class ElectricHeater(Appliance):
    WATTS = Power(600)
    EFFICIENCY = 0.1
    should_activate = False
    name = 'ElectricHeater'

    def __init__(self):
        super().__init__()

    def generate_heat(self, energy: Energy) -> Temperature:
        heat = energy * self.EFFICIENCY
        # print(f'Generated Heat: {heat}')

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel) -> Energy:
        self.on = self.should_activate
        if self.should_activate:
            energy_demand = self.get_energy_demand()
            self.usage += energy_demand
            self.generate_heat(energy_demand)
            return energy_demand
        else:
            return Energy(0)

    def get_energy_demand(self) -> Energy:
        # return self.WATTS / self.TO_WATT_HOURS
        return self.WATTS * Time.from_minutes(10)

    def activate(self):
        self.should_activate = True

    def reset(self):
        self.should_activate = False
