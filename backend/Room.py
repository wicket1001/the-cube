WEIGHT_AIR = 1.293
SPECIFIC_HEAT_CAPACITY = 1.01
# https://de.wikipedia.org/wiki/Spezifische_W%C3%A4rmekapazit%C3%A4t
TO_WATT_HOURS = 6
SECONDS = 60
HOURS = 60




class Room:
    # quadratic_metres = 40
    length = 5
    width = 8
    room_height = 2.5

    def __init__(self):
        pass

    def get_quadratic_metres(self):
        return self.length * self.width

    def get_surface(self):
        return self.length * self.room_height * 2 + self.width * self.room_height * 2

    def __str__(self):
        return 'Room'

    def heating(self, heat_power):  # in Watts
        """
        Heats a room with a given power

        :param heat_power: in Watts
        :return: delta T in Kelvin
        """
        # c = kJ / (kg*K)
        # K = kJ / (c*kg)
        kilo_joule = self.joule_10min(heat_power) / 1000
        delta_t = kilo_joule / (SPECIFIC_HEAT_CAPACITY * self.weight_air())
        return delta_t

    def joule_10min(self, heat_power):
        to_watt_hours = (HOURS * SECONDS) / TO_WATT_HOURS
        power = to_watt_hours * heat_power  # WATT * 10min (Wh)
        return power

    def weight_air(self):
        weight = self.litre_air() * WEIGHT_AIR / 1000  # kg
        return weight

    def litre_air(self):
        volume = self.get_quadratic_metres() * self.room_height  # m3
        litre = volume * 1000  # dm3 or l
        return litre

    def adapt_to_outside(self, outside, inside):
        delta = (outside - inside) * 0.1
        return delta
