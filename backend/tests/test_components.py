#!/usr/bin python3
# encoding=utf-8

# python test_components.py TestComponents
# python test_components.py TestComponents.test_solar_panel

import unittest
import csv
from datetime import datetime

from ElectricHeater import ElectricHeater
from HeatPump import HeatPump
from Physics import *
from Room import Room
from SolarPanel import SolarPanel


class TestComponents(unittest.TestCase):
    STEPS_PER_DAY = 144
    outer_temperatures = []
    dates = []
    radiations = []
    winds = []

    @classmethod
    def setUpClass(cls):
        with open('../res/Messstationen Zehnminutendaten v2 Datensatz_20210101T0000_20240101T0000.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            headers = reader.__next__()
            date_index = headers.index('time')
            radiation_index = headers.index('cglo')
            temperature_index = headers.index('tl')
            wind_index = headers.index('ff')
            for row in reader:
                cls.dates.append(datetime.fromisoformat(row[date_index]))
                try:
                    cls.radiations.append(float(row[radiation_index]))
                except ValueError:
                    cls.radiations.append(0)
                cls.outer_temperatures.append(float(row[temperature_index]))
                cls.winds.append(float(row[wind_index]))

    def tearDown(self):
        pass

    def test_sin_solar_panel(self):
        solar_panel = SolarPanel(1)
        energy = Energy(0)
        for i in range(self.STEPS_PER_DAY):
            production_step = solar_panel.step(i, i)
            energy += production_step
        self.assertAlmostEqual(energy.value, 9166.96, places=2)
        # solar_panel.print_statistics()
        self.assertEqual(solar_panel.watt_sum.value, 0)

    def test_simulated_solar_panel(self):
        solar_energy = 31443600  # EXCEL
        solar_panel = SolarPanel(1)
        solar_panel.save_weather(self.radiations)
        energy = Energy(0)

        night = [0] * 19
        right_watts = night + [7, 14, 29, 50, 72, 93, 122]
        right_joule = [(600 * x * solar_panel.SOLAR_EFFICIENCY) for x in right_watts]

        date_to_explore = datetime(2022, 5, 31, 0, 0, 0, 0)
        day = date_to_explore.timetuple()[7] + 365 - 1
        for step in range(self.STEPS_PER_DAY):
            absolute_step = day * self.STEPS_PER_DAY + step
            production_step = solar_panel.step(step, absolute_step)
            # print(production_step)
            if step < len(right_watts):
                self.assertEqual(production_step.value, right_joule[step])
            energy += production_step
        self.assertEquals(solar_panel.generation.value, solar_energy * solar_panel.SOLAR_EFFICIENCY)
        self.assertEquals(solar_panel.solar_energy.value, solar_energy)
        watt_average = solar_panel.watt_sum / self.STEPS_PER_DAY
        self.assertAlmostEquals(watt_average.value, 363.93, places=2)
        self.assertEqual(str(watt_average), '363.93W')
        self.assertEqual(energy.format_kilo_watt_hours(), '1.75kWh')
        self.assertEquals(energy.format_watt_day(), '72.79Wd')

        watt_per_second = (watt_average * solar_panel.SOLAR_EFFICIENCY) / Time.from_hours(1)
        self.assertAlmostEquals(watt_per_second.value, 0.02, places=3)
        self.assertEquals(str(watt_per_second), '0.02W')
        watt_per_day = watt_per_second * Time.from_hours(24).value
        self.assertAlmostEquals(watt_per_day.value, 1746.87, places=2)
        self.assertEqual(str(watt_per_day), '1746.87W')
        self.assertEqual(watt_per_day.format_kilo_watt(), '1.75kW')

    def test_electric_heater(self):
        electric_heater = ElectricHeater()
        energy = electric_heater.step(0)
        self.assertEquals(energy.value, 0)
        electric_heater.activate()
        energy = electric_heater.step(1)
        electric_heater.reset()
        self.assertEquals(energy.value, Energy.from_watt_hours(2000 / 6).value)
        energy = electric_heater.step(2)
        self.assertEquals(energy.value, 0)

    def test_heating(self):
        room = Room(8, 5, 2.5)
        room.SPECIFIC_HEAT_CAPACITY = SpecificHeatCapacity(20)
        radiator = Power(2400)
        temperature = room.heat_hour(radiator)
        self.assertAlmostEqual(temperature.value, 3.341, places=3)  # B7

    def test_heating_loss(self):
        # Tested with calculations in Excel
        room = Room(8, 5, 2.5)
        furniture = SpecificHeatCapacity(20)
        room.SPECIFIC_HEAT_CAPACITY = furniture

        inside = Temperature.from_celsius(21)
        outside = Temperature.from_celsius(0)
        delta_t = outside - inside

        heating_loss_power_per_m2 = room.heat_loss_power_per_m2(delta_t)
        self.assertAlmostEqual(heating_loss_power_per_m2.value, 6.77, places=2)  # G17

        heating_loss_power = room.get_heat_loss_power(delta_t)
        self.assertAlmostEqual(heating_loss_power.value, 982.26, places=2)  # G18

        heating_loss_energy = room.get_heat_loss_energy(delta_t)
        self.assertAlmostEqual(heating_loss_energy.value, 3536129, places=1)  # G19

        # heating_loss_temperature = furniture.calculate_heat(heating_loss_energy, room.mass)
        heating_loss_temperature = room.heat_hour(heating_loss_power)
        self.assertAlmostEqual(heating_loss_temperature.value, 1.3674, places=4)  # C7

        heating_loss_temperature2 = room.heat_loss_hour(outside, inside)
        self.assertAlmostEqual(heating_loss_temperature2.value, heating_loss_temperature.value)

    def test_lossy_heating(self):
        heat_applied = 1.97  # D7

        room = Room(8, 5, 2.5)
        furniture = SpecificHeatCapacity(20)
        room.SPECIFIC_HEAT_CAPACITY = furniture
        radiator = Power(2400)

        inside = Temperature.from_celsius(21)
        outside = Temperature.from_celsius(0)
        delta_t = outside - inside

        temperature = room.heat_hour(radiator)
        self.assertAlmostEqual(temperature.value, 3.341, places=3)  # B7

        heating_loss_power = room.get_heat_loss_power(delta_t)
        heating_loss_temperature = room.heat_hour(heating_loss_power)
        self.assertAlmostEqual(heating_loss_temperature.value, 1.3674, places=4)  # C7

        heated_temperature = temperature - heating_loss_temperature
        self.assertAlmostEqual(heated_temperature.value, heat_applied, places=2)  # D7

        radiator_power = radiator * Time.from_hours(1)  # I8
        heating_loss_energy = room.get_heat_loss_energy(delta_t)
        self.assertAlmostEqual(heating_loss_energy.value, 3536129, places=1)  # G19
        lossy_heat_energy = radiator_power - heating_loss_energy
        heated_temperature2 = furniture.calculate_heat(lossy_heat_energy, room.mass)
        self.assertAlmostEqual(heated_temperature2.value, heat_applied, places=2)  # D7

        self.assertAlmostEqual(heated_temperature.value, heated_temperature2.value)

        heated_temperature3 = room.lossy_heat_hour(radiator, outside, inside)
        self.assertAlmostEqual(heated_temperature3.value, heat_applied, places=2)  # D7
        self.assertAlmostEqual(heated_temperature.value, heated_temperature3.value)

    def test_cooling(self):
        room = Room(8, 5, 2.5)
        room.SPECIFIC_HEAT_CAPACITY = SpecificHeatCapacity(20)
        delta_t = room.adapt_to_outside(Temperature(0), Temperature(21))
        self.assertEquals(delta_t.value, -2.1)

    def test_heat_pump(self):
        heat_pump = HeatPump()


if __name__ == '__main__':
    unittest.main()
