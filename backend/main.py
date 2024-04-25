import csv
from datetime import datetime

from DebugLevel import DebugLevel
from Physics import *
from Fridge import Fridge
from Lights import Lights
from SolarPanel import SolarPanel
from Battery import Battery
from ElectricHeater import ElectricHeater
from Grid import Grid
from Room import Room

STEPS_PER_DAY = int((24 * 60) / 10)

solarPanel = SolarPanel(1)
battery = Battery()
electricHeater = ElectricHeater()
lights = Lights()
fridge = Fridge()
grid = Grid()
room = Room(5, 8, 2.5)
money = Money(0)
energy_production = Energy(0)
energy_consumption = Energy(0)
appliances = [electricHeater, lights, fridge]
inner_temperature = Temperature(21)
outer_temperature = Temperature(3)
dates = []
outer_temperatures = []
radiations = []
winds = []
verbosity = DebugLevel.INFORMATIONAL


def get_energy_demand(t: int):
    energy_demand = Energy(0)
    for appliance in appliances:
        energy_demand += appliance.step(t)
    return energy_demand


def step(step_of_the_day: int, absolute_step: int):
    global money
    global energy_consumption, energy_production
    global inner_temperature
    global outer_temperature
    outer_temperature = Temperature(0)

    natural_cooling = room.adapt_to_outside(outer_temperature, inner_temperature)
    inner_temperature += natural_cooling

    if inner_temperature < Temperature(19.5):
        electricHeater.activate()
        delta_t = room.heat(electricHeater.WATTS)
        inner_temperature += delta_t
    if verbosity >= DebugLevel.DEBUGGING:
        print(f'Inner temperature: {inner_temperature}')

    energy_demand = get_energy_demand(step_of_the_day)
    energy_consumption += energy_demand
    energy_supply = solarPanel.step(step_of_the_day, absolute_step)
    energy_production += energy_supply
    if verbosity >= DebugLevel.DEBUGGING:
        print(f'Energy demand: {energy_demand}, energy supply: {energy_supply}')

    if energy_demand > energy_supply:
        over_demand = energy_demand - energy_supply
        if battery.battery_level > Energy(0):
            if over_demand > battery.battery_level:
                over_demand -= battery.battery_level
                battery.take(battery.battery_level)
                money -= grid.buy(over_demand)
                if verbosity >= DebugLevel.DEBUGGING:
                    print(f'Bought {over_demand} energy')
                electricHeater.generate_heat(energy_demand)
            else:
                battery.take(over_demand)
                if verbosity >= DebugLevel.DEBUGGING:
                    print(f'Took everything from battery {battery}, took {over_demand}')
                electricHeater.generate_heat(energy_demand)
        else:
            money -= grid.buy(over_demand)
            if verbosity >= DebugLevel.DEBUGGING:
                print(f'Bought {over_demand} energy because battery is empty')
            electricHeater.generate_heat(energy_demand)

    else:
        energy_overproduction = energy_supply - energy_demand
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'Energy overproduction: {energy_overproduction}')
        electricHeater.generate_heat(energy_demand)
        battery_overfull = battery.store(energy_overproduction)
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'Selling: {battery_overfull}')
        money += grid.sell(battery_overfull)
    if verbosity >= DebugLevel.DEBUGGING:
        print(battery)

    # calculate_heat_power_demand()

    electricHeater.reset()


def calculate_heat_power_demand():
    area = 20  # m^2
    # https://www.heizsparer.de/heizung/heiztechnik/heizleistung-berechnen
    u_value = 3.1
    delta_t = 3
    # q_value = area * u_value * delta_t
    q_value = 2000
    delta_t = q_value / (area * u_value)


def main():
    with open('res/Messstationen Zehnminutendaten v2 Datensatz_20210101T0000_20240101T0000.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = reader.__next__()
        # print(headers)
        date_index = headers.index('time')
        radiation_index = headers.index('cglo')
        temperature_index = headers.index('tl')
        wind_index = headers.index('ff')
        if verbosity >= DebugLevel.DEBUGGING:
            print(date_index, radiation_index, temperature_index, wind_index)
        for row in reader:
            # print(len(row), ', '.join(row))
            dates.append(datetime.fromisoformat(row[date_index]))
            try:
                radiations.append(float(row[radiation_index]))
            except ValueError:
                radiations.append(0)
            outer_temperatures.append(float(row[temperature_index]))
            winds.append(float(row[wind_index]))

    if verbosity >= DebugLevel.DEBUGGING:
        print(len(dates), ', '.join([x.strftime('%d.%m.%Y %H:%M') for x in dates]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(radiations), ', '.join([str(x) for x in radiations]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(outer_temperatures), ', '.join([str(x) for x in outer_temperatures]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(winds), ', '.join([str(x) for x in winds]))
    solarPanel.save_weather(radiations)

    trying = 365
    for day in range(trying):
        date_to_explore = datetime(2022, 5, 31, 0, 0, 0, 0)
        if trying == 1:
            day = date_to_explore.timetuple()[7] + 365 - 1
        print(f'Day {day}')
        for i in range(STEPS_PER_DAY):
            absolute_step = day * STEPS_PER_DAY + i
            if verbosity >= DebugLevel.NOTIFICATION:
                print(f'\nDay {day}, relative Step {i}, absolute Step {absolute_step}, {dates[absolute_step]}')
            step(i, absolute_step)
    print('\n---------')
    grid.print_statistics(verbosity)
    electricHeater.print_statistics()
    # solarPanel.print_statistics()
    # fridge.print_statistics()
    lights.print_statistics()
    print(f'Money: {money}') # 4,18

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
