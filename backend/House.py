from Appliance import Appliance
from DebugLevel import DebugLevel
from Generator import Generator
from HeatPump import HeatPump
from Physics import *
from Fridge import Fridge
from Lights import Lights
from SandBattery import SandBattery
from SolarPanel import SolarPanel
from Battery import Battery
from ElectricHeater import ElectricHeater
from Grid import Grid
from Room import Room
from SolarThermal import SolarThermal
from WaterBuffer import WaterBuffer
from Windturbine import Windturbine
from algorithm_utils import Season, Algorithms

STEPS_PER_DAY = int((24 * 60) / 10)


def to_co2(energy: Energy) -> float:
    # https://www.rensmart.com/Calculators/KWH-to-CO2
    return (energy.value / 1000.0) * 0.076


class House(object):
    solarPanel: SolarPanel = None # SolarPanel(12 * 24)  # m^2
    windturbine: Windturbine = None # Windturbine(24 * 0.5, 0)  # m^2
    solarThermal: SolarThermal = None
    battery: Battery = None # Battery(Energy.from_kilo_watt_hours(200))
    sand_battery: SandBattery = None # SandBattery(1, 1, 1)
    water_buffer: WaterBuffer = None
    heatPump: HeatPump = None
    grid = Grid()
    money = Money(0)
    co2 = 0  # TODO CO2 unit
    energy_production = Energy(0)
    energy_consumption = Energy(0)
    # generators = [solarPanel, windturbine]
    outer_temperature = Temperature(0)
    patched_temperature = None
    outer_temperature_patch = None
    rooms = []

    def get_energy_demand(self, repsponse: dict, t: int, absolute_step: int, verbosity: DebugLevel):
        energy_demand = Energy(0)
        appliances_response = []
        for appliance in self.get_appliances():
            appliance_demand = appliance.step(t, absolute_step, verbosity)
            energy_demand += appliance_demand
            appliances_response.append({
                'name': appliance.name,
                'demand': appliance_demand,
                'usage': appliance.usage,
                'on': appliance.on
            })
        return energy_demand

    def get_appliances(self) -> [Appliance]:
        return [self.heatPump]

    def get_energy_production(self, response: dict, t: int, absolute_step: int, verbosity: DebugLevel):
        energy_produced = Energy(0)
        generators_response = []
        for generator in self.get_generators():
            energy_supply = generator.step(t, absolute_step, verbosity)
            energy_produced += energy_supply
            generators_response.append({
                'name': generator.name,
                'supply': energy_supply,
                'generation': generator.generation
            })
        response["generators"] = generators_response
        return energy_produced

    def get_generators(self) -> [Generator]:
        return self.solarPanel, self.windturbine, self.solarThermal

    def valid(self) -> bool:
        valid = True
        for room in self.rooms:
            # print(f'{room.name} is {room.valid()}')
            if not room.valid():
                valid = False
        return valid

    def set_rooms(self, rooms: [Room]):
        self.rooms = rooms
        self.heatPump.flow_rate = Length.from_litre(0)
        for room in self.rooms:
            self.heatPump.flow_rate += room.radiator.litres

    def heat_loss(self, outside) -> Energy:
        energy_sum = Energy(0)
        for room in self.rooms:
            energy_loss = room.surrounding_loss(outside, room.temperature)
            # print(f'{room.name}: {energy_loss.format_watt_hours()}')
            energy_sum += energy_loss
        return energy_sum

    def update_temperatures(self) -> None:
        for room in self.rooms:
            # print(f'{room.name}: before {room.temperature.format_celsius()}', end='')
            # diff = room.temperature - room.next_temperature
            # diff_energy = room.room_shc.calculate_energy(diff, room.mass)
            room.update_temperatures()
            # print(f' {room.name}: after {room.temperature.format_celsius()}', end='')
            # print(f'--> {diff} {diff_energy.format_watt_hours()}')
            # print(f'"{room.name}";{room.temperature.format_celsius()}')

    def step(self, step_of_the_day: int, absolute_step: int, algorithms: Algorithms, weather, verbosity: DebugLevel) -> dict:
        response = {
            'rooms': []
        }
        self.reset_before()

        temp = Temperature.from_celsius(weather['temperatures'][absolute_step])
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'temp={temp}')
            print(f'patched_temperature={self.patched_temperature}')
            print(f'outer_temperature={self.outer_temperature}')
            print(f'outer_temperature_patch{self.outer_temperature_patch}')

        temp = self.patch_outside_temperature(temp, verbosity)

        self.outer_temperature = temp
        # response['environment']['temperatures'] = self.outer_temperature # TODO

        # natural_cooling = self.room.adapt_to_outside(self.outer_temperature, self.inner_temperature)
        # self.inner_temperature += natural_cooling
        # natural_cooling = self.room.heat_loss(self.outer_temperature, self.inner_temperature)
        # self.inner_temperature -= natural_cooling
        self.heat_loss(self.outer_temperature)
        self.update_temperatures()

        # self.inner_temperature += occupants.get_heat()

        for room in self.rooms:
            room.step(step_of_the_day, absolute_step, algorithms, verbosity)

        energy_demand = Energy(0)
        if self.water_buffer.temperature < Temperature.from_celsius(80):
            # print(self.heatPump.flow_rate.format_litre())
            weight, temperature = self.water_buffer.take_water(self.heatPump.flow_rate)
            self.heatPump.input_water(self.heatPump.flow_rate, temperature)
            self.heatPump.activate()
            energy_demand += self.heatPump.step(step_of_the_day, absolute_step, verbosity)
            self.heatPump.deactivate()
            weight, temperature = self.heatPump.output_water()
            self.water_buffer.add_water(self.heatPump.flow_rate, temperature)

        back_weight = []
        back_temperatures = []
        for i, room in enumerate(self.rooms):
            if room.temperature < Temperature.from_celsius(19):
                room.radiator.activate()
            if room.radiator.should_activate:
                weight, temperature = self.water_buffer.take_water(room.radiator.litres * room.radiators)
                temperature, power = room.radiator.getRadiatorData(temperature, room.temperature, room.radiator.flow_rate)
                back_weight.append(weight * room.radiators)
                back_temperatures.append(temperature)
                delta_t = room.heat(power * Time.from_minutes(10) * room.radiators)
                # print(delta_t)
                room.temperature += delta_t
        back_temperatures_index = 0
        for i, room in enumerate(self.rooms):
            if room.radiator.should_activate:
                self.water_buffer.add_water(room.radiator.litres * room.radiators, back_temperatures[back_temperatures_index])
                back_temperatures_index += 1
            room.radiator.deactivate()
        # print(self.water_buffer.temperature.format_celsius())

        # if algorithms == Algorithms.BENCHMARK:
        # elif algorithms == Algorithms.DECISION_TREE:
        # else:
        #    raise NotImplementedError('No other Algorithm is implemented.')

        for room in self.rooms:
            energy_demand_room = room.get_energy_demand(
                response,
                step_of_the_day,
                absolute_step,
                verbosity
            )
            energy_demand += energy_demand_room
        self.energy_consumption += energy_demand
        energy_supply = self.get_energy_production(
            response,
            step_of_the_day,
            absolute_step,
            verbosity
        )  # solarPanel.step(step_of_the_day, absolute_step)
        self.energy_production += energy_supply
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'Energy demand: {energy_demand}, energy supply: {energy_supply}')

        self.algorithm_callback(absolute_step, energy_demand, energy_supply, algorithms, verbosity)

        if verbosity >= DebugLevel.DEBUGGING:
            print(self.battery)

        # calculate_heat_power_demand()

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
        self.co2 += to_co2(self.grid.buying)
        response['co2'] = self.co2  # TODO bought gas
        response['money'] = self.money

        self.reset_after()

        return response

    def reset_before(self):
        self.grid.reset()
        for room in self.rooms:
            room.reset_before()

    def reset_after(self):
        for room in self.rooms:
            # room.electricHeater.deactivate()
            room.radiator.deactivate()

    def patch_outside_temperature(self, temp, verbosity):
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
        return temp

    def get_season(self, absolute_step: int) -> Season:
        absolute_step %= STEPS_PER_DAY * 365
        if 0 <= absolute_step < STEPS_PER_DAY * 90:
            return Season.SPRING
        elif STEPS_PER_DAY * 90 <= absolute_step < STEPS_PER_DAY * 181:
            return Season.SUMMER
        elif STEPS_PER_DAY * 181 <= absolute_step < STEPS_PER_DAY * 273:
            return Season.FALL
        elif STEPS_PER_DAY * 273 <= absolute_step < STEPS_PER_DAY * 365:
            return Season.WINTER
        else:
            raise NotImplementedError('Something went wrong in the implementation of the seasons.')

    def get_capacity(self) -> (Battery.Status, Battery.Status):
        t_status = self.battery.get_status()
        return t_status, Battery.Status.EMPTY

    def charge_battery(self,
                       total_energy_surplus: Energy,
                       total_energy_surplus_COP: Energy,
                       priority: str,
                       battery: Battery,
                       sand_battery: SandBattery):
        wasted_surplus = 0
        if priority == 'eBattery':
            if battery.battery_level < battery.capacity:
                battery.store(total_energy_surplus_COP)
            if battery.battery_level > battery.capacity and sand_battery.battery_level <= sand_battery.capacity:
                # sand_battery.
                pass

    def algorithm_callback(self, absolute_step, energy_demand: Energy, energy_supply: Energy, algorithm: Algorithms,
                           verbosity: DebugLevel):
        if algorithm == Algorithms.BENCHMARK:
            if energy_demand > energy_supply:
                over_demand = energy_demand - energy_supply
                if self.battery.battery_level > Energy(0):
                    if over_demand > self.battery.battery_level:
                        over_demand -= self.battery.battery_level
                        self.battery.take(self.battery.battery_level)
                        self.money -= self.grid.buy(over_demand)
                        if verbosity >= DebugLevel.DEBUGGING:
                            print(f'Bought {over_demand} energy')
                        # self.electricHeater.generate_heat(energy_demand)
                    else:
                        self.battery.take(over_demand)
                        if verbosity >= DebugLevel.DEBUGGING:
                            print(f'Took everything from battery {self.battery}, took {over_demand}')
                        # self.electricHeater.generate_heat(energy_demand)
                else:
                    self.money -= self.grid.buy(over_demand)
                    if verbosity >= DebugLevel.DEBUGGING:
                        print(f'Bought {over_demand} energy because battery is empty')
                    # self.electricHeater.generate_heat(energy_demand)

            else:
                energy_overproduction = energy_supply - energy_demand
                if verbosity >= DebugLevel.DEBUGGING:
                    print(f'Energy overproduction: {energy_overproduction}')
                # self.electricHeater.generate_heat(energy_demand)
                battery_overfull = self.battery.store(energy_overproduction)
                if verbosity >= DebugLevel.DEBUGGING:
                    print(f'Selling: {battery_overfull}')
                self.money += self.grid.sell(battery_overfull)
        elif algorithm == Algorithms.MATLAB:
            season = self.get_season(absolute_step)
            t_status, e_status = self.get_capacity()
            if verbosity >= DebugLevel.INFORMATIONAL:
                print(f't_status: {t_status}')

            if season == Season.SPRING:
                if t_status == Battery.Status.CHARGING and e_status == Battery.Status.EMPTY:
                    pass

            elif season == Season.WINTER:
                total_energy_surplus = 0
                total_energy_surplus_cop = 0
                priority = 0
                if t_status == Battery.Status.CHARGING and e_status == Battery.Status.EMPTY:
                    if energy_demand > energy_supply:
                        self.charge_battery(
                            total_energy_surplus,
                            total_energy_surplus_cop,
                            priority,
                            self.battery,
                            self.sand_battery
                        )
        elif algorithm == Algorithms.DECISION_TREE:
            if energy_demand > energy_supply:
                over_demand = energy_demand - energy_supply
                if self.battery.battery_level > Energy(0):
                    if over_demand > self.battery.battery_level:
                        over_demand -= self.battery.battery_level
                        self.battery.take(self.battery.battery_level)
                        self.money -= self.grid.buy(over_demand)
                        if verbosity >= DebugLevel.DEBUGGING:
                            print(f'Bought {over_demand} energy')
                        # self.electricHeater.generate_heat(energy_demand)
                    else:
                        self.battery.take(over_demand)
                        if verbosity >= DebugLevel.DEBUGGING:
                            print(f'Took everything from battery {self.battery}, took {over_demand}')
                        # self.electricHeater.generate_heat(energy_demand)
                else:
                    self.money -= self.grid.buy(over_demand)
                    if verbosity >= DebugLevel.DEBUGGING:
                        print(f'Bought {over_demand} energy because battery is empty')
                    # self.electricHeater.generate_heat(energy_demand)

            else:
                energy_overproduction = energy_supply - energy_demand
                if verbosity >= DebugLevel.DEBUGGING:
                    print(f'Energy overproduction: {energy_overproduction}')
                # self.electricHeater.generate_heat(energy_demand)
                battery_overfull = self.battery.store(energy_overproduction)
                if verbosity >= DebugLevel.DEBUGGING:
                    print(f'Selling: {battery_overfull}')
                self.money += self.grid.sell(battery_overfull)
        else:
            raise NotImplementedError('No more Algorithms implemented.')

    def patch_outer_temperature(self, outer_temp):
        self.patched_temperature = Temperature(30) + self.outer_temperature
        self.outer_temperature = self.patched_temperature
        self.outer_temperature_patch = Temperature(30) / (Time.from_hours(12) / Time.from_minutes(10))  # Goback to normal through 12h
        print(f'{outer_temp=}')
        print(f'patched_temperature={self.patched_temperature}')
        print(f'outer_temperature={self.outer_temperature}')
        print(f'outer_temperature_patch{self.outer_temperature_patch}')
