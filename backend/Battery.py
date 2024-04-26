from Physics import Power, Energy


class Battery:
    capacity = Energy.from_kilo_watt_hours(13.5)
    efficiency = 0.85

    def __init__(self):
        self.battery_level = Energy(0)
        self.stored = Energy(0)
        self.taken = Energy(0)

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

        if energy + self.battery_level > self.capacity:
            print("Battery full")
            diff = self.capacity - self.battery_level
            self.battery_level += diff
            return energy - diff
        else:
            self.battery_level += energy
            return Energy(0)

    def take(self, energy: Energy):
        if energy < Energy(0):
            raise ValueError("Energy")
        if energy > self.battery_level:
            raise ValueError("Battery")
        self.battery_level -= energy

