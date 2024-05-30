import math

from Appliance import Appliance
from DebugLevel import DebugLevel
from Physics import Energy, Time


class Equipment(Appliance):
    name = 'Equipment'
    STEPS_PER_DAY = 144
    factors = []

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def __init__(self, watts: float):
        super().__init__(watts)
        self.energy_bob = self.WATTS * Time.from_minutes(10)

        sigmoid_start = -6
        sigmoid_step = (24 / self.STEPS_PER_DAY)
        step = sigmoid_start
        for i in range(self.STEPS_PER_DAY):
            value = self.sigmoid(step) / (self.STEPS_PER_DAY / 2)
            self.factors.append(value)
            step += sigmoid_step
            if step >= 6:
                sigmoid_step *= -1

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        energy_demand = Energy(self.factors[t] * self.energy_bob.value)
        self.usage += energy_demand
        return energy_demand
