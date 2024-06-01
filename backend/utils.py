import csv
from datetime import datetime

from Battery import Battery
from DebugLevel import DebugLevel
from ElectricHeater import ElectricHeater
from Equipment import Equipment
from HeatPump import HeatPump
from House import House
from Lights import Lights
from Occupancy import Occupancy
from Physics import Length, Energy, Temperature
from Radiator import Radiator
from Room import Room
from SandBattery import SandBattery
from SolarPanel import SolarPanel
from SolarThermal import SolarThermal
from WaterBuffer import WaterBuffer
from Windturbine import Windturbine


def read_mat(verbosity: DebugLevel):
    # https://stackoverflow.com/questions/874461/read-mat-files-in-python
    pass


def read_csv(verbosity: DebugLevel):
    weather = {
        'dates': [],
        'radiations': [],
        'temperatures': [],
        'winds': [],
        'wind_directions': [],
        'precipitations': []
    }

    with open('res/Messstationen Zehnminutendaten v2 Datensatz_20210101T0000_20240101T0000.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = reader.__next__()
        # print(headers)
        date_index = headers.index('time')
        radiation_index = headers.index('cglo')
        temperature_index = headers.index('tl')
        wind_index = headers.index('ff')
        wind_direction_index = headers.index('dd')
        precipitation_index = headers.index('rr')
        if verbosity >= DebugLevel.DEBUGGING:
            print(date_index, radiation_index, temperature_index, wind_index, precipitation_index)
        for row in reader:
            # print(len(row), ', '.join(row))
            weather['dates'].append(datetime.fromisoformat(row[date_index]))
            try:
                weather['radiations'].append(float(row[radiation_index]))
            except ValueError:
                weather['radiations'].append(0)
            weather['temperatures'].append(float(row[temperature_index]))
            weather['winds'].append(float(row[wind_index]))
            weather['wind_directions'].append(float(row[wind_direction_index]))
            weather['precipitations'].append(float(row[precipitation_index]))

    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['dates']), ', '.join([x.strftime('%d.%m.%Y %H:%M') for x in weather['dates']]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['radiations']), ', '.join([str(x) for x in weather['radiations']]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['temperatures']), ', '.join([str(x) for x in weather['temperatures']]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['winds']), ', '.join([str(x) for x in weather['winds']]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['precipitation']), ', '.join([str(x) for x in weather['precipitation']]))

    return weather


def get_house():
    cellar_left = Room(6, 24, 4, Occupancy.Predefined.EMPTY, name='Cellar left')
    cellar_right = Room(6, 24, 4, Occupancy.Predefined.EMPTY, name='Cellar right')
    first_left = Room(6, 24, 4, Occupancy.Predefined.HIGH, name='First left')
    first_right = Room(6, 24, 4, Occupancy.Predefined.HIGH, name='First right')
    second_left = Room(6, 24, 4, Occupancy.Predefined.MEDIUM, name='Second left')
    second_right = Room(6, 24, 4, Occupancy.Predefined.MEDIUM, name='Second right')
    third_left = Room(6, 24, 4, Occupancy.Predefined.HIGH, name='Third left')
    third_right = Room(6, 24, 4, Occupancy.Predefined.HIGH, name='Third right')
    attic_left = Room(6, 24, 5, Occupancy.Predefined.LOW, name='Attic left')
    attic_right = Room(6, 24, 5, Occupancy.Predefined.LOW, name='Attic right')
    cellar_left.set_surfaces(Room.Surface.UNDEFINED,
                             Room.Surface.GROUND,
                             Room.Surface.GROUND,
                             Room.Surface.UNDEFINED,
                             Room.Surface.GROUND,
                             Room.Surface.GROUND)
    cellar_right.set_surfaces(Room.Surface.UNDEFINED,
                              Room.Surface.GROUND,
                              Room.Surface.UNDEFINED,
                              Room.Surface.GROUND,
                              Room.Surface.GROUND,
                              Room.Surface.GROUND)
    attic_left.set_surfaces(Room.Surface.OUTSIDE,
                            Room.Surface.UNDEFINED,
                            Room.Surface.OUTSIDE,
                            Room.Surface.UNDEFINED,
                            Room.Surface.OUTSIDE,
                            Room.Surface.OUTSIDE)
    attic_right.set_surfaces(Room.Surface.OUTSIDE,
                             Room.Surface.UNDEFINED,
                             Room.Surface.UNDEFINED,
                             Room.Surface.OUTSIDE,
                             Room.Surface.OUTSIDE,
                             Room.Surface.OUTSIDE)
    for room in [first_left, second_left, third_left]:
        room.set_surfaces(Room.Surface.UNDEFINED,
                          Room.Surface.UNDEFINED,
                          Room.Surface.OUTSIDE,
                          Room.Surface.UNDEFINED,
                          Room.Surface.OUTSIDE,
                          Room.Surface.OUTSIDE)
    for room in [first_right, second_right, third_right]:
        room.set_surfaces(Room.Surface.UNDEFINED,
                          Room.Surface.UNDEFINED,
                          Room.Surface.UNDEFINED,
                          Room.Surface.OUTSIDE,
                          Room.Surface.OUTSIDE,
                          Room.Surface.OUTSIDE)
    cellar_left.link_right(cellar_right, True)
    cellar_left.link_top(first_left, True)
    cellar_right.link_top(first_right, True)
    attic_right.link_left(attic_left, True)
    attic_right.link_bottom(third_right, True)
    attic_left.link_bottom(third_left, True)
    second_left.link_right(second_right, True)
    second_left.link_top(third_left, True)
    second_left.link_bottom(first_left, True)
    second_right.link_top(third_right, True)
    second_right.link_bottom(first_right, True)
    first_left.link_right(first_right, True)
    third_right.link_left(third_left, True)
    rooms = [cellar_left, cellar_right,
             first_left, first_right,
             second_left, second_right,
             third_left, third_right,
             attic_left, attic_right]
    house = House()
    for room in rooms:
        # print(room.get_volume().format_qubic_metres())
        room.lights = Lights(room.get_lights_estimation().value)
        # room.electricHeater = ElectricHeater(600)
        room.radiator = Radiator()
        room.radiators = 2
        # room.radiator.set_flow_rate(Length.from_litre(room.radiator.flow_rate.value * 10_000))  #  / 100 * 576
        room.equipment = Equipment(room.get_equipment_estimation().value)
    house.heatPump = HeatPump(10_000)
    house.set_rooms(rooms)
    house.solarPanel = SolarPanel(Length(12 * 24 * 0.5))
    house.windturbine = Windturbine(24 * 0.5, 0)
    house.solarThermal = SolarThermal(Length(12 * 24 * 0.5))
    house.battery = Battery(Energy.from_kilo_watt_hours(200))
    house.sand_battery = SandBattery(1, 1, 1)
    house.water_buffer = WaterBuffer(Length.from_litre(1000), Temperature.from_celsius(80))
    return house
