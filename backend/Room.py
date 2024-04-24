import numbers

from Physics import Power, Temperature, Energy, Time, Length, SpecificHeatCapacity, Density, Weight

# https://www.heizsparer.de/heizung/heiztechnik/heizleistung-berechnen
# Q [Heizleistung W] = Wohnfläche [m^2] * U-Wert [W/(m^2*K)] * Temperaturdifferenz [delta K]
# U-Wert [W/(m^2*K)]
u_value = {
    'Passivhaus': 0.1,
    'Niedrigenergiehaus': 0.15,
    'Gebäude mit Außenhülle nach EnEV 2016': 0.35,
    'Gebäude mit Außenhülle nach EnEV 2009': 1.09,
    'Gebäude mit Außenhülle nach EnEV 2002': 1.29,
    'Gebäude mit Außenhplle nach WSchV 1995': 1.91,
    'Gebäude mit Außenhülle nach DIN 4701': 2.83,
    'Altbau 1977 - 1983': 3.1,
    'Altbau 1970 - 1976': 4.29,
    'Altbau ab 1969': 4.66,
    'Altbau ab 1959': 5.06,
    'Altbau vor 1949 (Lehm-Holzfachwerk)': 5,
    'Altbau vor 1949 (Ziegelvollmauerwerk)': 5.24
}

# WEIGHT_AIR = 1.293
SPECIFIC_HEAT_CAPACITY = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.AIR) # 1.01
# https://de.wikipedia.org/wiki/Spezifische_W%C3%A4rmekapazit%C3%A4t
# TO_WATT_HOURS = 6
# SECONDS = 60
# HOURS = 60


class Room:
    # quadratic_metres = 40
    length = Length(0)
    width = Length(0)
    room_height = Length(0)
    mass = Weight(0)

    def __init__(self,
                 length: [numbers.Number, Length],
                 width: [numbers.Number, Length],
                 room_height: [numbers.Number, Length]):
        if isinstance(length, numbers.Number):
            self.length = Length(float(length))
        elif isinstance(length, Length):
            self.length = length
        else:
            raise NotImplementedError('length')

        if isinstance(width, numbers.Number):
            self.width = Length(float(width))
        elif isinstance(width, Length):
            self.width = width
        else:
            raise NotImplementedError('width')

        if isinstance(room_height, numbers.Number):
            self.room_height = Length(float(room_height))
        elif isinstance(room_height, Length):
            self.room_height = room_height
        else:
            raise NotImplementedError('room_height')

        air = Density.from_predefined(Density.Predefined.AIR)
        print(self.get_volume())
        self.mass = air.calculate_mass(self.get_volume())
        print(self.mass)

    def get_quadratic_metres(self):
        return self.length * self.width

    def get_mantle(self):
        return (self.length * self.room_height * 2 +
                self.width * self.room_height * 2)

    def get_surface(self):
        return (self.length * self.room_height * 2 +
                self.width * self.room_height * 2 +
                self.length * self.width * 2)

    def get_volume(self):
        return self.length * self.width * self.room_height

    def get_litre(self):
        return self.get_volume() * 1000

    def __str__(self):
        return 'Room'

    def heating(self, heat_power: Power) -> Temperature:  # in Watts
        """
        Heats a room with a given power

        :param heat_power: in Watts
        :return: delta T in Kelvin
        """
        # c = kJ / (kg*K)
        # K = kJ / (c*kg)
        # kilo_joule = self.joule_10min(heat_power) / 1000
        # delta_t = kilo_joule / (SPECIFIC_HEAT_CAPACITY * self.weight_air())
        # return delta_t
        return SPECIFIC_HEAT_CAPACITY.calculate_heat(heat_power * Time.from_minutes(10), self.mass)

    def joule_10min(self, heat_power: Power) -> Energy:
        # to_watt_hours = (HOURS * SECONDS) / TO_WATT_HOURS
        # power = to_watt_hours * heat_power  # WATT * 10min (Wh)
        return heat_power * Time.from_minutes(10)

    # def weight_air(self) -> float:
    #     weight = (self.litre_air().value * WEIGHT_AIR / 1000)  # kg
    #     return weight
    #
    # def litre_air(self) -> Length:
    #     volume = self.get_quadratic_metres() * self.room_height  # m3
    #     litre = volume * 1000  # dm3 or l
    #     return litre

    def adapt_to_outside(self, outside: Temperature, inside: Temperature) -> Temperature:
        delta = (outside - inside) * 0.1
        return delta
