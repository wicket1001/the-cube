from enum import IntFlag, auto

from Physics import Power, Energy


class Battery:
    class Status(IntFlag):
        EMPTY = auto()
        CHARGING = auto()
        FULL = auto()

    capacity = Energy(0)
    efficiency = 0.85

    def __init__(self, capacity: Energy):
        self.battery_level = Energy(0)
        self.stored = Energy(0)  # Stored in total over the lifetime of the battery
        self.taken = Energy(0)  # Taken in total over the lifetime of the battery, should be 0.85 * stored
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
            # print("Battery full")
            diff = self.capacity - self.battery_level
            self.battery_level += diff
            self.stored += diff
            return energy - diff / self.efficiency
        else:
            self.battery_level += energy * self.efficiency
            self.stored += energy
            return Energy(0)

    def take(self, energy: Energy):
        if energy < Energy(0):
            raise ValueError("Energy")
        if energy > self.battery_level:
            raise ValueError("Battery")
        self.taken += energy
        self.battery_level -= energy

    def percentage(self) -> float:
        return self.battery_level.value / self.capacity.value
    
    def get_status(self) -> Status:
        if 0 <= self.battery_level.value < self.capacity.value * 0.2:
            status = Battery.Status.EMPTY
        elif self.capacity.value * 0.2 <= self.battery_level.value < self.capacity.value * 0.8:
            status = Battery.Status.CHARGING
        elif self.capacity.value * 0.8 <= self.battery_level.value <= self.capacity.value:
            status = Battery.Status.FULL
        else:
            raise NotImplementedError('Something went wrong in the implementation of the capacity.')
        return status
