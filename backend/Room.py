import numbers
import warnings
from enum import IntFlag, auto

from Occupancy import Occupancy
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
    class Surface(IntFlag):
        UNDEFINED = auto()
        OUTSIDE = auto()
        GROUND = auto()
    top = Surface.UNDEFINED
    bottom = Surface.UNDEFINED
    left = Surface.UNDEFINED
    right = Surface.UNDEFINED
    front = Surface.UNDEFINED
    back = Surface.UNDEFINED
    # surfaces = [top, bottom, left, right, front, back]

    name = ''

    SPECIFIC_HEAT_CAPACITY = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.AIR)  # 1.01
    # https://de.wikipedia.org/wiki/Spezifische_W%C3%A4rmekapazit%C3%A4t

    u_value = 3.10
    p_value = 1 / u_value
    energy_pass = 77  # kWh / (m^2 * year)

    length = Length(0)
    width = Length(0)
    room_height = Length(0)
    mass = Weight(0)
    SIMULATION_TIME_STEP = Time.from_minutes(10)
    INITIAL_TEMPERATURE_C = 19
    temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)

    surfaces_names = ['top', 'bottom', 'left', 'right', 'front', 'back']
    wall_u_value = 0.29
    roof_u_value = 0.25
    flooring_u_value = 0.2 # to outside
    inner_wall_u_value = 1
    inner_ceiling_u_value = 0.85
    inner_flooring_u_value = 0.7 # to inside
    ground_u_value = 1
    outside_u_values = [roof_u_value, flooring_u_value, wall_u_value, wall_u_value, wall_u_value, wall_u_value]
    inside_u_values = [inner_ceiling_u_value, inner_flooring_u_value,
                       inner_wall_u_value, inner_wall_u_value,
                       inner_wall_u_value, inner_wall_u_value]

    INITIAL_TEMPERATURE_C = 19
    current_heat = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    next_temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)

    room_shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.AIR)

    def __init__(self,
                 length: [numbers.Number, Length],
                 width: [numbers.Number, Length],
                 room_height: [numbers.Number, Length],
                 occupancy: Occupancy.Predefined = Occupancy.Predefined.EMPTY,
                 name: str = ''):
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

        self.occupancy = Occupancy.from_predefined(occupancy, self.get_quadratic_metres())

        self.name = name

    def valid_surface(self, surface) -> bool:
        if isinstance(surface, Room.Surface):
            return True
        return False

    def surface_index_to_name(self, i: int) -> str:
        return self.surfaces_names[i]

    def set_top(self, top):
        if not self.valid_surface(top):
            raise AttributeError('Unsupported surface type.')
        self.top = top

    def set_bottom(self, bottom):
        if not self.valid_surface(bottom):
            raise AttributeError('Unsupported surface type.')
        self.bottom = bottom

    def set_left(self, left):
        if not self.valid_surface(left):
            raise AttributeError('Unsupported surface type.')
        self.left = left

    def set_right(self, right):
        if not self.valid_surface(right):
            raise AttributeError('Unsupported surface type.')
        self.right = right

    def set_front(self, front):
        if not self.valid_surface(front):
            raise AttributeError('Unsupported surface type.')
        self.front = front

    def set_back(self, back):
        if not self.valid_surface(back):
            raise AttributeError('Unsupported surface type.')
        self.back = back

    def get_surfaces(self) -> tuple:
        return self.top, self.bottom, self.left, self.right, self.front, self.back

    def set_surfaces(self, top, bottom, left, right, front, back) -> None:
        self.set_top(top)
        self.set_bottom(bottom)
        self.set_left(left)
        self.set_right(right)
        self.set_front(front)
        self.set_back(back)

    def valid(self) -> bool:
        """
        Tests if the room is valid, returns false if otherwise.
        TODO should not be checked by server rather than client

        :return: True if valid, False otherwise.
        """
        for i, surface in enumerate(self.get_surfaces()):  # self.surfaces:
            if isinstance(surface, Room.Surface):
                if surface == Room.Surface.UNDEFINED:
                    raise AttributeError(f'{self.name}/{self.surface_index_to_name(i)} is not defined.')
        for i, surface in enumerate(self.get_surfaces()):
            if i == 1:
                continue
            if surface == Room.Surface.GROUND:
                warnings.warn(f'{self.name} surface {self.surface_index_to_name(i)} other than bottom is {Room.Surface.GROUND}.')
                # return False
                # raise AttributeError(f'{surface} should not be {Room.Surface.GROUND}.')
        return True

    def link_top(self, rooms, recursive) -> None:
        if isinstance(rooms, Room):
            rooms = [rooms]
        elif not isinstance(rooms, list):
            raise AttributeError('Rooms is no instance of list or Room')
        self.top = rooms
        if recursive:
            for room in rooms:
                room.link_bottom(self, False)

    def link_bottom(self, rooms, recursive) -> None:
        if isinstance(rooms, Room):
            rooms = [rooms]
        elif not isinstance(rooms, list):
            raise AttributeError('Rooms is no instance of list or Room')
        self.bottom = rooms
        if recursive:
            for room in rooms:
                room.link_top(self, False)

    def link_left(self, rooms, recursive) -> None:
        if isinstance(rooms, Room):
            rooms = [rooms]
        elif not isinstance(rooms, list):
            raise AttributeError('Rooms is no instance of list or Room')
        self.left = rooms
        if recursive:
            for room in rooms:
                room.link_right(self, False)

    def link_right(self, rooms, recursive) -> None:
        if isinstance(rooms, Room):
            rooms = [rooms]
        elif not isinstance(rooms, list):
            raise AttributeError('Rooms is no instance of list or Room')
        self.right = rooms
        if recursive:
            for room in rooms:
                room.link_left(self, False)

    def link_front(self, rooms, recursive) -> None:
        if isinstance(rooms, Room):
            rooms = [rooms]
        elif not isinstance(rooms, list):
            raise AttributeError('Rooms is no instance of list or Room')
        self.front = rooms
        if recursive:
            for room in rooms:
                room.link_back(self, False)

    def link_back(self, rooms, recursive) -> None:
        if isinstance(rooms, Room):
            rooms = [rooms]
        elif not isinstance(rooms, list):
            raise AttributeError('Rooms is no instance of list or Room')
        self.back = rooms
        if recursive:
            for room in rooms:
                room.link_front(self, False)

    def surrounding_loss(self, outside: Temperature, inside: Temperature) -> Energy:
        delta_t = inside - outside
        # print(outside.format_celsius(), inside.format_celsius(), delta_t)
        sum_p_value = Power(0)
        sum_energy = Energy(0)
        for i, surface in enumerate(self.get_surfaces()):
            if isinstance(surface, self.Surface):
                if surface == self.Surface.UNDEFINED:
                    raise ValueError(f'Undefined Surface at {self.surface_index_to_name(i)} in {self.name}')
                p_value = Power(self.outside_u_values[i] * self.get_surface_area(i).value * delta_t.value)
                # print(self.outside_u_values[i], self.get_surface_area(i), delta_t, p_value)
                sum_p_value += p_value
            elif isinstance(surface, Room):
                raise NotImplementedError('Pls implement')
            elif isinstance(surface, list):
                for s in surface:
                    if isinstance(s, Room):
                        room_difference = abs(s.temperature - self.temperature)
                        if room_difference > Temperature(0.01):
                            wall = self.get_surface_area(i)
                            # print(wall.format_square_metres())
                            #opposing_wall = s.get_surface_area(self.get_opposite_surface(i))
                            #wall = min(wall, opposing_wall)
                            p_value = Power(self.inside_u_values[i] * wall.value * room_difference.value)
                            #print(p_value)
                            energy_transfer = p_value * self.SIMULATION_TIME_STEP
                            if s.temperature > self.temperature:
                                sum_energy += energy_transfer
                            else:
                                sum_energy -= energy_transfer
                    else:
                        raise ValueError(f'List Undefined Surface type at {self.surface_index_to_name(i)} in {self.name} as {surface}')
            else:
                raise ValueError(f'Undefined Surface type at {self.surface_index_to_name(i)} in {self.name} as {surface}')
        p_energy_loss = sum_p_value * self.SIMULATION_TIME_STEP
        # print(p_energy_loss, sum_energy, p_energy_loss + sum_energy)
        # if sum_energy.value > 0:
        #     print(f'Energy gained at {self.name}')
        # else:
        #     print(f'Energy lost at {self.name}')
        total_energy_lost = p_energy_loss - sum_energy
        # print('AMBIENT LOSS', p_energy_loss.format_watt_hours())
        # print('EXCHANGE LOSS', sum_energy.format_watt_hours())
        heat_transfer = self.room_shc.calculate_heat(total_energy_lost, self.mass)
        self.next_temperature = self.temperature - heat_transfer
        return total_energy_lost

    def heat_exchange(self, outside: Temperature, inside: Temperature) -> Energy:
        sum_energy = Energy(0)
        for i, surface in enumerate(self.get_surfaces()):
            if isinstance(surface, self.Surface):
                continue
            elif isinstance(surface, Room):
                raise NotImplementedError('Pls implement')
            elif isinstance(surface, list):
                for s in surface:
                    if isinstance(s, Room):
                        delta_t = abs(s.temperature - self.temperature)
                        if delta_t > Temperature(0.01):
                            wall = self.get_surface_area(i)
                            # print(wall.format_square_metres())
                            #opposing_wall = s.get_surface_area(self.get_opposite_surface(i))
                            #wall = min(wall, opposing_wall)
                            p_value = Power(self.inside_u_values[i] * wall.value * delta_t.value)
                            #print(p_value)
                            energy_transfer = p_value * self.SIMULATION_TIME_STEP
                            # print(energy_transfer.format_watt_hours())
                            # print(self.mass)
                            heat_transfer = self.room_shc.calculate_heat(energy_transfer, self.mass)
                            # print(heat_transfer)
                            # print('other', s.temperature.format_celsius())
                            # print('self', self.temperature.format_celsius())
                            if s.temperature > self.temperature:
                                s.next_temperature = s.temperature - heat_transfer
                                self.next_temperature = self.temperature + heat_transfer
                                # print('other', s.next_heat.format_celsius())
                                # print('self', self.next_heat.format_celsius())
                                if not s.next_temperature > self.next_temperature:
                                    warnings.warn('The hotter cube switched around')
                                    raise ValueError('The hotter cube switched around')
                            else:
                                s.next_temperature = s.temperature + heat_transfer
                                self.next_temperature = self.temperature - heat_transfer
                                # print('other', s.next_heat.format_celsius())
                                # print('self', self.next_heat.format_celsius())
                                if not s.next_temperature < self.next_temperature:
                                    warnings.warn('The hotter cube switched around')
                                    raise ValueError('The hotter cube switched around')
                    else:
                        raise ValueError(f'List Undefined Surface type at {self.surface_index_to_name(i)} in {self.name} as {surface}')
            else:
                raise ValueError(f'Undefined Surface type at {self.surface_index_to_name(i)} in {self.name} as {surface}')

    def update_temperatures(self):
        self.temperature = self.next_temperature
        self.next_temperature = Temperature.from_celsius(self.INITIAL_TEMPERATURE_C)

    def get_quadratic_metres(self) -> Length:
        return self.length * self.width

    def get_mantle(self) -> Length:
        return (self.length * self.room_height * 2 +
                self.width * self.room_height * 2)

    def get_surface(self) -> Length:
        return (self.length * self.room_height * 2 +
                self.width * self.room_height * 2 +
                self.length * self.width * 2)

    def get_volume(self) -> Length:
        return self.length * self.width * self.room_height

    def get_litre(self) -> Length:
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

    def get_surface_area(self, i) -> Length:
        return (self.width * self.length,
                self.width * self.length,
                self.width * self.room_height,
                self.width * self.room_height,
                self.length * self.room_height,
                self.length * self.room_height)[i]

    def get_opposite_surface(self, i: int) -> int:
        return (1, 0, 3, 2, 5, 4)[i]
