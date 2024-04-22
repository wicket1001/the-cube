

class Battery:
    capacity = 80
    efficiency = 0.85

    def __init__(self):
        self.battery_level = 0
        self.stored = 0
        self.taken = 0

    def __str__(self):
        return f'Battery {self.battery_level}'

    def store(self, energy: float):
        """
        Stores energy into the battery.

        :param energy:
        :return: How much energy overflows.
        """
        if energy < 0:
            raise ValueError("Energy")

        if energy + self.battery_level > self.capacity:
            print("Battery full")
            diff = self.capacity - self.battery_level
            self.battery_level += diff
            return energy - diff
        else:
            self.battery_level += energy
            return 0

    def take(self, energy: float):
        if energy < 0:
            raise ValueError("Energy")
        if energy > self.battery_level:
            raise ValueError("Battery")
        self.battery_level -= energy

