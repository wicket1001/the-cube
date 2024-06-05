import json
import math
import time

import utils
from DebugLevel import DebugLevel
from Physics import *
from algorithm_utils import Algorithms
from utils import get_house, Strips, Colors, mapper, write_boundaries

STEPS_PER_DAY = int((24 * 60) / 10)

verbosity = DebugLevel.EMERGENCY

#maxlen = max([len(x) for x in colors])
maxi_value = {}
mini_value = {}


def peaks(strip: Strips, value: float):
    if strip in maxi_value.keys():
        if value > maxi_value[strip]:
            maxi_value[strip] = value
    else:
        maxi_value[strip] = value
    if strip in mini_value.keys():
        if value < mini_value[strip]:
            mini_value[strip] = value
    else:
        mini_value[strip] = value


gridding = {'pos': Energy(0), 'neg': Energy(0), 'neutral': Energy(0)}
gridding2 = {'pos': 0, 'neg': 0, 'neutral': 0}

def serial_control(response: dict):
    value = mapper(response['benchmark']['grid']['diff'].value, Energy.from_watt_hours(10).value, Energy.from_watt_hours(5).value, -1, 1)
    peaks(Strips.GRID, response['benchmark']['grid']['diff'].value)
    if response['benchmark']['grid']['diff'].value > 0:
        gridding['pos'] += response['benchmark']['grid']['buy']
        gridding2['pos'] += 1
    elif response['benchmark']['grid']['diff'].value < 0:
        # print(response['benchmark']['grid']['diff'].format_watt_hours(), response['benchmark']['grid']['sell'].format_watt_hours(), response['benchmark']['grid']['buy'].format_watt_hours())
        gridding['neg'] += response['benchmark']['grid']['sell']
        gridding2['neg'] += 1
    else:
        gridding['neutral'] += Energy(0)
        gridding2['neutral'] += 1

    value = mapper(response['benchmark']['battery']['diff'].value, Energy.from_watt_hours(10).value,
                        Energy.from_watt_hours(5).value, -1, 1)
    peaks(Strips.BATTERY, response['benchmark']['battery']['diff'].value)
    for generator in response['benchmark']['generators']:
        if generator['name'] == 'Windturbine':
            value = mapper(generator['supply'].value, 0, Energy.from_watt_hours(5).value, 1, 0)
            peaks(Strips.WIND_TURBINE, generator['supply'].value)
        elif generator['name'] == 'SolarPanel':
            value = mapper(generator['supply'].value, 0, Energy.from_watt_hours(1000).value, 1, 0)
            peaks(Strips.SOLAR_PANEL, generator['supply'].value)
        elif generator['name'] == 'SolarThermal':
            value = mapper(generator['supply'].value, 0, Energy.from_watt_hours(1000).value, 1, 0)
            peaks(Strips.SOLAR_THERMAL_WATER, generator['supply'].value)
    room_demand = []
    room_radiator = []
    for i, room in enumerate(response['benchmark']['rooms']):
        sum = Energy(0)
        for appliance in room['appliances']:
            sum += appliance['demand']
        room_demand.append(sum)
        room_radiator.append(room['radiator'])
    # TODO
    cumulative = Energy(0)
    radiator = False
    room_index = 0
    for i in range(len(room_demand) - 1, -1, -1):  # 0 is on purpose as there is no FIRST UP
        value = mapper(room_demand[i].value, 0, Energy.from_watt_hours(5).value, 1, 0)
        index = Strips.ATTIC_RIGHT + room_index
        # print(index)
        peaks(index, room_demand[i].value)
        cumulative += room_demand[i]
        if room_radiator[i]:
            radiator = True
        room_index += 1
        if i % 2 == 0:
            value = mapper(cumulative.value, 0, Energy.from_watt_hours(5).value, 1, 0)
            peaks(Strips.ATTIC_RIGHT + room_index, cumulative.value)
            # cumulative = Energy(0)
            value = 0.5
            peaks(Strips.THIRD_RADIATORS - (6 - math.floor(room_index / 3)), 0.5)
            # radiator = False  # does not make sense as there is no energy flow in between otherwise
            room_index += 1
            peaks(Strips.THIRD_RADIATORS - (6 - math.ceil(room_index / 3)), 0.5)
    value = mapper(response['benchmark']['HeatPump']['demand'].value, Energy.from_watt_hours(6).value,
                        Energy.from_watt_hours(5).value, 1, 0)
    peaks(Strips.HEATPUMP, response['benchmark']['HeatPump']['demand'].value)


def main():
    # https://de.wikipedia.org/wiki/Building_Management_System
    weather = utils.read_csv(verbosity)
    all = [e.name for e in Strips]
    max_boundaries, min_boundaries = utils.get_boundaries()
    print(max_boundaries)
    print(min_boundaries)
    for maxi in sorted(max_boundaries.keys()):
        try:
            if isinstance(maxi, Strips):
                name = maxi.name
            else:
                name = all[maxi - 1]
        except IndexError:
            name = maxi
        print(
            f'{name:>30}, {maxi:2}, {max_boundaries[maxi].format_watt_hours():>20}, {min_boundaries[maxi].format_watt_hours():>20}')

    benchmark_house = get_house()


    benchmark_house.solarPanel.save_weather(weather['radiations'])
    benchmark_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])
    benchmark_house.solarThermal.save_weather(weather['radiations'], weather['winds'], weather['temperatures'])

    decision_house = get_house()
    decision_house.solarPanel.save_weather(weather['radiations'])
    decision_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])
    decision_house.solarThermal.save_weather(weather['radiations'], weather['winds'], weather['temperatures'])

    benchmark_house.solarThermal.input_water(Length.from_litre(1_000_000), Temperature.from_celsius(7))
    decision_house.solarThermal.input_water(Length.from_litre(1_000_000), Temperature.from_celsius(7))

    trying = 365
    start = time.time()
    print(maxi_value)
    print(mini_value)
    for day in range(trying):
        date_to_explore = datetime(2022, 5, 31, 0, 0, 0, 0)
        if trying == 1:
            # day = date_to_explore.timetuple()[7] + 365 - 1
            pass
        if verbosity >= DebugLevel.WARNING:
            print(f'Day {day}')
        for i in range(STEPS_PER_DAY):
            absolute_step = day * STEPS_PER_DAY + i
            if verbosity >= DebugLevel.NOTIFICATION:
                print(f'\nDay {day}, relative Step {i}, absolute Step {absolute_step}, {weather["dates"][absolute_step]}')

            response = {
                'step': i,
                'absolute_step': absolute_step,
                'environment': {},
                'benchmark': {},
                'decision': {}
            }
            for condition in weather.keys():
                response['environment'][condition] = weather[condition][absolute_step]
                if condition == 'temperatures':
                    response['environment']['temperatures'] = Temperature.from_celsius(response['environment']['temperatures'])

            benchmark = benchmark_house.step(i, absolute_step, Algorithms.BENCHMARK, weather, verbosity)
            decision = decision_house.step(i, absolute_step, Algorithms.DECISION_TREE, weather, verbosity)

            response['benchmark'] = benchmark
            response['decision'] = decision
            if verbosity >= DebugLevel.NOTIFICATION:
                print(json.dumps(response, cls=SIEncoder))  # , indent=4
            serial_control(response)
    for x in gridding.keys():
        print(x, gridding[x].format_kilo_watt_hours())
    for x in gridding2.keys():
        print(x, gridding2[x])
    print(maxi_value)
    print(mini_value)
    all = [e.name for e in Strips]
    for maxi in sorted(maxi_value.keys()):
        try:
            if isinstance(maxi, Strips):
                name = maxi.name
            else:
                name = all[maxi - 1]
        except IndexError:
            name = maxi
        print(f'{name:>30}, {maxi:2}, {Energy(maxi_value[maxi]).format_watt_hours():>20}, {Energy(mini_value[maxi]).format_watt_hours():>20}')
    write_boundaries(maxi, maxi_value, mini_value)
    end = time.time()
    print(end - start, 's')
    print('\n---------')
    benchmark_house.grid.print_statistics(verbosity)
    # benchmark_house.electricHeater.print_statistics()
    benchmark_house.solarPanel.print_statistics()
    benchmark_house.windturbine.print_statistics()
    #benchmark_house.equipment.print_statistics()
    #benchmark_house.lights.print_statistics()
    print(f'Money: {benchmark_house.money}') # 4,18

    print(f'CO2: {benchmark_house.co2}')
    print(f'CO2: {decision_house.co2}')


#     print("""
# ---------
# RIGHT:
# Bought: 4216.05kWh for 401.71€
# Sold: 3.42kWh for 0.08€
# Diff: 4212.63kWh for 401.62€
# Used: 4482000.0Wh
# Produced: 269342.67Wh
# Money: -401.62
# ---------
# RIGHT after physics rework:
# Bought: 5157.42kWh for 491.40€
# Sold: 68.76kWh for 1.64€
# Diff: 5088.66kWh for 489.76€
# Used: 4482000.00Wh
# Produced: 269342.67Wh
# Money: -489.76€
#     """)


if __name__ == '__main__':
    main()
