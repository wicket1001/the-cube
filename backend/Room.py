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


class Room:
    SPECIFIC_HEAT_CAPACITY = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.AIR)  # 1.01
    # https://de.wikipedia.org/wiki/Spezifische_W%C3%A4rmekapazit%C3%A4t

    u_value = 3.10
    p_value = 1 / u_value

    length = Length(0)
    width = Length(0)
    room_height = Length(0)
    mass = Weight(0)
    SIMULATION_TIME_STEP = Time.from_minutes(10)

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
        # print(self.get_volume())
        self.mass = air.calculate_mass(self.get_volume())
        # print(self.mass)

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

    def lossy_heat(self, heat_power: Power, outside: Temperature, inside: Temperature) -> Temperature:
        return self.lossy_heat_hour(heat_power, outside, inside) / (Time.from_hours(1) / self.SIMULATION_TIME_STEP)

    def lossy_heat_hour(self, heat_power: Power, outside: Temperature, inside: Temperature) -> Temperature:
        return self.heat_hour(heat_power) - self.heat_loss_hour(outside, inside)

    def heat_loss(self, outside: Temperature, inside: Temperature) -> Temperature:
        return self.heat_loss_hour(outside, inside) / (Time.from_hours(1) / self.SIMULATION_TIME_STEP)

    def heat_loss_hour(self, outside: Temperature, inside: Temperature) -> Temperature:
        delta_t = outside - inside
        heat_loss_power = self.get_heat_loss_power(delta_t)
        return self.heat_hour(heat_loss_power)

    def heat_hour(self, heat_power: Power) -> Temperature:
        """
        Heats a room with a given power for an hour.

        :param heat_power: in Watts
        :return: delta T in Kelvin
        """
        # c = kJ / (kg*K)
        # K = kJ / (c*kg)
        # kilo_joule = self.joule_10min(heat_power) / 1000
        # delta_t = kilo_joule / (SPECIFIC_HEAT_CAPACITY * self.weight_air())
        # return delta_t
        return self.SPECIFIC_HEAT_CAPACITY.calculate_heat(heat_power * Time.from_hours(1), self.mass)

    def heat(self, heat_power: Power) -> Temperature:  # in Watts
        return self.heat_hour(heat_power) / (Time.from_hours(1) / self.SIMULATION_TIME_STEP)

    def get_heat_loss_energy(self, delta_t: Temperature) -> Energy:
        return self.get_heat_loss_power(delta_t) * Time.from_hours(1)

    def get_heat_loss_power(self, delta_t: Temperature) -> Power:
        return Power(self.heat_loss_power_per_m2(delta_t).value * self.get_surface().value)

    def heat_loss_power_per_m2(self, delta_t: Temperature) -> Power:
        return Power(self.p_value * abs(delta_t.value))  # TODO

    def adapt_to_outside(self, outside: Temperature, inside: Temperature) -> Temperature:
        delta = (outside - inside) * 0.1
        return delta
