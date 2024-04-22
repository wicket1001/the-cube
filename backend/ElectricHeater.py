from Appliance import Appliance


class ElectricHeater(Appliance):
    WATTS = 2000
    EFFICIENCY = 0.1
    should_activate = False

    def __init__(self):
        super().__init__()

    def generate_heat(self, energy: float):
        heat = energy * self.EFFICIENCY
        # print(f'Generated Heat: {heat}')

    def step(self, t: int):
        if self.should_activate:
            energy_demand = self.get_energy_demand()
            self.usage += energy_demand
            self.generate_heat(energy_demand)
            return energy_demand
        else:
            return 0

    def get_energy_demand(self):
        return self.WATTS / self.TO_WATT_HOURS

    def activate(self):
        self.should_activate = True

    def reset(self):
        self.should_activate = False
