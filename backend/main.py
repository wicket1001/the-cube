import json
import time

import utils
from DebugLevel import DebugLevel
from House import House
from Physics import *
from algorithm_utils import Algorithms
from utils import get_house

STEPS_PER_DAY = int((24 * 60) / 10)

verbosity = DebugLevel.NOTIFICATION


def main():
    # https://de.wikipedia.org/wiki/Building_Management_System
    weather = utils.read_csv(verbosity)
    benchmark_house = get_house()

    benchmark_house.solarPanel.save_weather(weather['radiations'])
    benchmark_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])

    decision_house = get_house()
    decision_house.solarPanel.save_weather(weather['radiations'])
    decision_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])

    trying = 365
    start = time.time()
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
    end = time.time()
    print(end - start, 's')
    print('\n---------')
    benchmark_house.grid.print_statistics(verbosity)
    benchmark_house.electricHeater.print_statistics()
    benchmark_house.solarPanel.print_statistics()
    benchmark_house.windturbine.print_statistics()
    benchmark_house.fridge.print_statistics()
    benchmark_house.lights.print_statistics()
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
