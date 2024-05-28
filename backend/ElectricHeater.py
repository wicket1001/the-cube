from Appliance import Appliance
from DebugLevel import DebugLevel
from Physics import Power, Time, Energy, Temperature


class ElectricHeater(Appliance):
    EFFICIENCY = 0.1
    should_activate = False
    name = 'ElectricHeater'

    def __init__(self, watts):
        super().__init__(watts)

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        self.on = self.should_activate
        if self.should_activate:
            energy_demand = self.get_energy_demand()
            self.usage += energy_demand
            # self.generate_heat(energy_demand)
            return energy_demand
        else:
            return Energy(0)

    def get_energy_demand(self) -> Energy:
        # return self.WATTS / self.TO_WATT_HOURS
        return self.WATTS * Time.from_minutes(10)

    def activate(self):
        self.should_activate = True

    def deactivate(self):
        self.should_activate = False
