#!/usr/bin python3
# encoding=utf-8

# python test_physics.py TestPhysics
# python test_physics.py TestPhysics.test_power

import unittest

from Physics import *
from Room import Room


class TestPhysics(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_time(self):
        time1 = Time(7200)
        self.assertEqual(time1.value, 7200)
        self.assertEqual(time1.format_minutes(), '120.00min')
        self.assertEqual(time1.format_hours(), '2.00h')

        time2 = Time.from_minutes(20)
        self.assertEqual(time2.value, 1200)
        self.assertEqual(time2.format_minutes(), '20.00min')

        time3 = Time.from_hours(2)
        self.assertEqual(time3.value, 7200)
        self.assertEqual(time3.format_hours(), '2.00h')

    def test_power(self):
        radiator_watt = Power(2000)
        self.assertEqual(radiator_watt.value, 2000)
        self.assertEqual(str(radiator_watt), '2000.00W')
        watt2 = Power.from_kilo_watt(2)
        self.assertEqual(watt2.value, 2000)
        self.assertEqual(watt2.format_kilo_watt(), '2.00kW')

    def test_energy(self):
        radiator_watt = Power(2000)
        radiator_energy = Time.from_hours(2) * radiator_watt
        self.assertEqual(radiator_energy.value, 14400000)
        self.assertEqual(str(radiator_energy), '14400000.00J')
        self.assertEqual(radiator_energy.format_watt_seconds(), '14400000.00Ws')
        self.assertEqual(radiator_energy.format_watt_hours(), '4000.00Wh')
        self.assertEqual(radiator_energy.format_kilo_watt_hours(), '4.00kWh')
        self.assertEqual(radiator_energy.format_watt_day(), '166.67Wd')
        self.assertEqual(radiator_energy.format_kilo_watt_day(), '0.17kWd')

        energy2 = Energy.from_watt_seconds(3600)
        self.assertEqual(energy2.value, 3600)
        self.assertEqual(energy2.format_watt_hours(), '1.00Wh')

        energy3 = Energy.from_watt_hours(1)
        self.assertEqual(energy3.value, 3600)
        self.assertEqual(energy3.format_watt_hours(), '1.00Wh')

        energy4 = Energy.from_kilo_watt_hours(1)
        self.assertEqual(energy4.value, 3600 * 1000)
        self.assertEqual(energy4.format_kilo_watt_hours(), '1.00kWh')

        energy5 = Energy.from_kilo_joule(2)
        self.assertEqual(energy5.value, 2000)
        self.assertEqual(energy5.format_kilo_joule(), '2.00kJ')

    def test_money(self):
        money = Money(100)
        self.assertEqual(money.value, 100)
        self.assertEqual(str(money), '100.00€')

        money2 = Money.from_cent(10)
        self.assertEqual(money2.value, 0.1)
        self.assertEqual(str(money2), '0.10€')

    def test_grid_calculations(self):
        price_per_kWh = Money.from_cent(10)
        usage = Energy.from_kilo_watt_hours(2)
        cost = price_per_kWh.calculate_kWh_cost(usage)
        self.assertEqual(cost.value, 0.2)
        # cost2 = usage * price_per_kWh
        # self.assertEqual(cost2.value, 0.2)

    def test_weight(self):
        weight = Weight(2000)
        self.assertEqual(weight.value, 2000)
        self.assertEqual(str(weight), '2000.00g')
        weight2 = Weight.from_kilo_gramm(2)
        self.assertEqual(weight2.value, 2000)
        self.assertEqual(weight2.format_kilo_gramm(), '2.00kg')

    def test_length(self):
        length = Length(5)
        width = Length(8)
        room_height = Length(2.5)
        self.assertEqual(length.value, 5)
        self.assertEqual(str(length), '5.00m')
        quadratic_metres = length * width
        self.assertEqual(quadratic_metres.value, 40)
        self.assertEqual(quadratic_metres.format_square_metres(), '40.00m^2')
        volume = quadratic_metres * room_height
        self.assertEqual(volume.value, 100)
        self.assertEqual(volume.format_qubic_metres(), '100.00m^3')

    def test_density(self):
        water = Density(1000)
        self.assertEqual(water.value, 1000)
        self.assertEqual(str(water), '1000.00ρ')
        concrete = Density.from_name('concrete')
        self.assertEqual(concrete.value, 2400)
        air = Density.from_predefined(Density.Predefined.AIR)
        self.assertEqual(air.value, 1.293)

        volume = Length(100)
        mass = air.calculate_mass(volume)
        self.assertEqual(str(mass), '129300.00g')
        self.assertEqual(mass.format_kilo_gramm(), '129.30kg')

        weight = Weight.from_kilo_gramm(129.3)
        volume2 = air.calculate_volume(weight)
        self.assertEqual(volume2.format_qubic_metres(), '100.00m^3')
        # self.assertEqual(volume2.format_qubic_metres())

    def test_room(self):
        room = Room(5, 8, 2.5)
        self.assertEqual(room.get_quadratic_metres().value, 40)
        self.assertEqual(room.get_mantle().value, 65)
        self.assertEqual(room.get_surface().value, 145)
        self.assertEqual(room.get_volume().value, 100)
        self.assertEqual(room.get_litre().value, 100000)
        air = Density.from_predefined(Density.Predefined.AIR)
        air_weight = air.calculate_mass(room.get_volume())
        self.assertAlmostEqual(air_weight.value, 129300)

    def test_specific_heat_capacity(self):
        water = SpecificHeatCapacity(4.18)
        self.assertEqual(water.value, 4.18)
        self.assertEqual(str(water), '4.18c')
        concrete = SpecificHeatCapacity.from_name('concrete')
        self.assertEqual(concrete.value, 0.88)
        wood_fiber_insulation = SpecificHeatCapacity.from_predefined(
            SpecificHeatCapacity.Predefined.WOOD_FIBER_INSULATION
        )
        self.assertEqual(wood_fiber_insulation.value, 2.1)

        room = Room(5, 8, 2.5)
        air = Density.from_predefined(Density.Predefined.AIR)
        mass = air.calculate_mass(room.get_volume())
        self.assertAlmostEqual(mass.value, 129300)

        radiator = Power(2400)
        radiator_energy = radiator * Time.from_hours(1)
        self.assertEqual(radiator_energy.value, 8640000)
        furniture = SpecificHeatCapacity(20)
        wanted_heat = Temperature(4)

        needed_energy = furniture.calculate_energy(
            wanted_heat,
            mass
        )
        self.assertAlmostEqual(needed_energy.value, Energy.from_kilo_joule(10344).value)

        generated_heat = furniture.calculate_heat(
            radiator_energy,
            mass
        )
        self.assertAlmostEqual(generated_heat.value, 3.341, places=3)

    def test_heatpump(self):
        shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.WATER)
        energy = shc.calculate_energy(Temperature(65) - Temperature(15), Weight(3000))
        print()
        print(energy.value / Time.from_minutes(10).value)


if __name__ == '__main__':
    unittest.main()
