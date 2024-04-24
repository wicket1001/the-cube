#!/usr/bin python3
# encoding=utf-8

# python test_components.py TestComponents
# python test_components.py TestComponents.test_solar_panel

import unittest
import csv
from datetime import datetime

from Physics import *
from SolarPanel import SolarPanel


class TestComponents(unittest.TestCase):
    STEPS_PER_DAY = 144
    outer_temperatures = []
    dates = []
    radiations = []
    winds = []

    def setUp(self):
        with open('../res/Messstationen Zehnminutendaten v2 Datensatz_20210101T0000_20240101T0000.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            headers = reader.__next__()
            date_index = headers.index('time')
            radiation_index = headers.index('cglo')
            temperature_index = headers.index('tl')
            wind_index = headers.index('ff')
            for row in reader:
                self.dates.append(datetime.fromisoformat(row[date_index]))
                try:
                    self.radiations.append(float(row[radiation_index]))
                except ValueError:
                    self.radiations.append(0)
                self.outer_temperatures.append(float(row[temperature_index]))
                self.winds.append(float(row[wind_index]))

    def tearDown(self):
        pass

    def test_sin_solar_panel(self):
        solar_panel = SolarPanel()
        energy = Energy(0)
        for i in range(self.STEPS_PER_DAY):
            production_step = solar_panel.step(i, i)
            energy += production_step
        self.assertAlmostEqual(energy.value, 9166.96, places=2)
        # solar_panel.print_statistics()
        self.assertEqual(solar_panel.watt_sum.value, 0)

    def test_simulated_solar_panel(self):
        solar_energy = 31443600  # EXCEL
        solar_panel = SolarPanel()
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
        self.assertEquals(solar_panel.production.value, solar_energy * solar_panel.SOLAR_EFFICIENCY)
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


if __name__ == '__main__':
    unittest.main()
