import csv
import json
from datetime import datetime

import utils
from DebugLevel import DebugLevel
from House import House
from Physics import *
from Fridge import Fridge
from Lights import Lights
from SolarPanel import SolarPanel
from Battery import Battery
from ElectricHeater import ElectricHeater
from Grid import Grid
from Room import Room
from Windturbine import Windturbine

STEPS_PER_DAY = int((24 * 60) / 10)

verbosity = DebugLevel.INFORMATIONAL


def main():
    weather = utils.read_csv(verbosity)
    house = House()

    house.solarPanel.save_weather(weather['radiations'])
    house.windturbine.save_weather(weather['winds'], weather['wind_directions'])

    trying = 365
    for day in range(trying):
        date_to_explore = datetime(2022, 5, 31, 0, 0, 0, 0)
        if trying == 1:
            # day = date_to_explore.timetuple()[7] + 365 - 1
            pass
        print(f'Day {day}')
        for i in range(STEPS_PER_DAY):
            absolute_step = day * STEPS_PER_DAY + i
            if verbosity >= DebugLevel.NOTIFICATION:
                print(f'\nDay {day}, relative Step {i}, absolute Step {absolute_step}, {weather["dates"][absolute_step]}')
            response = house.step(i, absolute_step, weather, verbosity)
            print(json.dumps(response, cls=SIEncoder))  # , indent=4
    print('\n---------')
    house.grid.print_statistics(verbosity)
    house.electricHeater.print_statistics()
    house.solarPanel.print_statistics()
    house.windturbine.print_statistics()
    house.fridge.print_statistics()
    house.lights.print_statistics()
    print(f'Money: {house.money}') # 4,18

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
