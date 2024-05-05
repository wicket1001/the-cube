from DebugLevel import DebugLevel
from Physics import *
from Fridge import Fridge
from Lights import Lights
from SolarPanel import SolarPanel
from Battery import Battery
from ElectricHeater import ElectricHeater
from Grid import Grid
from Room import Room
from Windturbine import Windturbine


class House(object):
    solarPanel = SolarPanel(1)  # m^2
    windturbine = Windturbine(75 * 0.5, 0)  # m^2
    battery = Battery()
    electricHeater = ElectricHeater(600)  # 600W
    lights = Lights(25)
    fridge = Fridge(150)
    grid = Grid()
    room = Room(5, 8, 2.5)  # m
    money = Money(0)
    energy_production = Energy(0)
    energy_consumption = Energy(0)
    appliances = [electricHeater, lights, fridge]
    generators = [solarPanel, windturbine]
    inner_temperature = Temperature(21)
    outer_temperature = Temperature(0)
    patched_temperature = None
    outer_temperature_patch = None

    def get_energy_production(self, response: dict, t: int, absolute_step: int, verbosity: DebugLevel):
        energy_produced = Energy(0)
        generators_response = []
        for generator in self.generators:
            energy_supply = generator.step(t, absolute_step, verbosity)
            energy_produced += energy_supply
            generators_response.append({
                'name': generator.name,
                'supply': energy_supply,
                'generation': generator.generation
            })
        response["generators"] = generators_response
        return energy_produced

    def get_energy_demand(self, response: dict, t: int, absolute_step: int, verbosity: DebugLevel):
        energy_demand = Energy(0)
        appliances_response = []
        for appliance in self.appliances:
            appliance_demand = appliance.step(t, absolute_step, verbosity)
            energy_demand += appliance_demand
            appliances_response.append({
                'name': appliance.name,
                'demand': appliance_demand,
                'usage': appliance.usage,
                'on': appliance.on
            })
        response["appliances"] = appliances_response
        return energy_demand

    def step(self, step_of_the_day: int, absolute_step: int, weather, verbosity: DebugLevel) -> dict:
        response = {'step': step_of_the_day, 'absolute_step': absolute_step, 'environment': {}}
        for condition in weather.keys():
            response['environment'][condition] = weather[condition][absolute_step]

        self.grid.reset()

        temp = Temperature(weather['temperatures'][absolute_step])
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'temp={temp}')
            print(f'patched_temperature={self.patched_temperature}')
            print(f'outer_temperature={self.outer_temperature}')
            print(f'outer_temperature_patch{self.outer_temperature_patch}')
        if self.patched_temperature is not None:
            diff = abs(self.outer_temperature - temp)
            if verbosity >= DebugLevel.DEBUGGING:
                print(f'diff={diff}')
                print(f'evaluate={diff < self.outer_temperature_patch}')
            if diff < self.outer_temperature_patch:
                self.patched_temperature = None
                self.outer_temperature_patch = None
            else:
                temp = self.outer_temperature - self.outer_temperature_patch

        self.outer_temperature = temp
        response['environment']['temperatures'] = self.outer_temperature

        natural_cooling = self.room.adapt_to_outside(self.outer_temperature, self.inner_temperature)
        self.inner_temperature += natural_cooling

        if self.inner_temperature < Temperature(19.5):
            self.electricHeater.activate()
            delta_t = self.room.heat(self.electricHeater.WATTS)
            self.inner_temperature += delta_t
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'Inner temperature: {self.inner_temperature}')

        response['environment']['inner_temperature'] = self.inner_temperature

        energy_demand = self.get_energy_demand(response, step_of_the_day, absolute_step, verbosity)
        self.energy_consumption += energy_demand
        energy_supply = self.get_energy_production(response, step_of_the_day,
                                              absolute_step, verbosity)  # solarPanel.step(step_of_the_day, absolute_step)
        self.energy_production += energy_supply
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'Energy demand: {energy_demand}, energy supply: {energy_supply}')

        if energy_demand > energy_supply:
            over_demand = energy_demand - energy_supply
            if self.battery.battery_level > Energy(0):
                if over_demand > self.battery.battery_level:
                    over_demand -= self.battery.battery_level
                    self.battery.take(self.battery.battery_level)
                    self.money -= self.grid.buy(over_demand)
                    if verbosity >= DebugLevel.DEBUGGING:
                        print(f'Bought {over_demand} energy')
                    self.electricHeater.generate_heat(energy_demand)
                else:
                    self.battery.take(over_demand)
                    if verbosity >= DebugLevel.DEBUGGING:
                        print(f'Took everything from battery {self.battery}, took {over_demand}')
                    self.electricHeater.generate_heat(energy_demand)
            else:
                self.money -= self.grid.buy(over_demand)
                if verbosity >= DebugLevel.DEBUGGING:
                    print(f'Bought {over_demand} energy because battery is empty')
                self.electricHeater.generate_heat(energy_demand)

        else:
            energy_overproduction = energy_supply - energy_demand
            if verbosity >= DebugLevel.DEBUGGING:
                print(f'Energy overproduction: {energy_overproduction}')
            self.electricHeater.generate_heat(energy_demand)
            battery_overfull = self.battery.store(energy_overproduction)
            if verbosity >= DebugLevel.DEBUGGING:
                print(f'Selling: {battery_overfull}')
            self.money += self.grid.sell(battery_overfull)
        if verbosity >= DebugLevel.DEBUGGING:
            print(self.battery)

        # calculate_heat_power_demand()

        self.electricHeater.reset()

        response['environment']['money'] = self.money
        response['battery'] = {
            'level': self.battery.battery_level,
            'stored': self.battery.stored,
            'taken': self.battery.taken
        }
        response['grid'] = {
            'sold': self.grid.sold,
            'bought': self.grid.bought,
            'sell': self.grid.selling,
            'buy': self.grid.buying
        }

        return response

    def patch_outer_temperature(self, outer_temp):
        self.patched_temperature = Temperature(30) + self.outer_temperature
        self.outer_temperature = self.patched_temperature
        self.outer_temperature_patch = Temperature(30) / (Time.from_hours(12) / Time.from_minutes(10))  # Goback to normal through 12h
        print(f'{outer_temp=}')
        print(f'patched_temperature={self.patched_temperature}')
        print(f'outer_temperature={self.outer_temperature}')
        print(f'outer_temperature_patch{self.outer_temperature_patch}')
