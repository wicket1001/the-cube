from Physics import Power, Energy


class Battery:
    capacity = Energy(0)
    efficiency = 0.85

    def __init__(self, capacity: Energy):
        self.battery_level = Energy(0)
        self.stored = Energy(0)
        self.taken = Energy(0)
        self.capacity = capacity

    def __str__(self):
        return f'Battery {self.battery_level}'

    def store(self, energy: Energy) -> Energy:
        """
        Stores energy into the battery.

        :param energy:
        :return: How much energy overflows.
        """
        if energy < Energy(0):
            raise ValueError("Energy")

        if energy * self.efficiency + self.battery_level > self.capacity:
            print("Battery full")
            diff = self.capacity - self.battery_level
            self.battery_level += diff
            self.stored += diff
            return energy - diff / self.efficiency
        else:
            self.battery_level += energy * self.efficiency
            self.stored += energy * self.efficiency
            return Energy(0)

    def take(self, energy: Energy):
        if energy < Energy(0):
            raise ValueError("Energy")
        if energy > self.battery_level:
            raise ValueError("Battery")
        self.taken += energy
        self.battery_level -= energy

