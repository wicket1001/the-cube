import math
import numbers
from typing import List

from DebugLevel import DebugLevel
from Generator import Generator
from Physics import Length, Energy, Power, Time, SpecificHeatCapacity, Density, Temperature, Weight


class SolarThermal(Generator):
    EFFICIENCY = 0.2 * 0.54
    WATER_EFFICIENCY = 0.85

    iterations = 0

    INITIAL_TEMPERATURE_C = 0
    solar_energy = Energy(0)
    radiations = []
    weight = Weight(0)
    temperature = Temperature.from_celsius(INITIAL_TEMPERATURE_C)
    density = Density.from_predefined(Density.Predefined.WATER)
    shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.WATER)

    name = "SolarThermal"
    litres = Length.from_litre(0)

    def __init__(self, size: [numbers.Number, Length]):
        super().__init__(size)

    def save_weather(self, array: List[float]):
        self.radiations = array

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL) -> Energy:
        if self.weight.value == 0:
            raise AttributeError('Water heated cannot be 0l.')
        self.iterations += 1
        radiation = self.radiations[absolute_step]
        watt = Power(radiation * self.area.value)
        joule = watt * Time.from_minutes(10)
        self.solar_energy += joule
        energy_production = joule * self.EFFICIENCY

        heat_production = joule * self.WATER_EFFICIENCY
        self.temperature += self.shc.calculate_heat(heat_production, self.weight)
        if verbosity >= DebugLevel.DEBUGGING:
            print(self.temperature.format_celsius())

        self.generation += energy_production
        return energy_production

    def get_solar_thermal_data(self, T_in, T_amb, V_flow, G, v_air, n):
        #Outputs: outlet temp in C and generated heat (Q) in W
        # Inputs: inlet temp in C, outside temp in C, volumetric flow rate in L/s,#
        # global irradiation in W/m^2, velocity of outside air in m/s, number of
        #solar thermal heaters in #

        # Water properties
        rho_mix = 1063  # kg/m^3, density of mix at 80C
        dyn_visc_mix = 0.0022  # kg/m.s, dynamic viscosity of mix at 80C
        k_mix = 0.444  # W/mK, thermal conductivity of mix at 80C
        Pr_mix = 2.22  # Prandtl number at 80C
        c_p_mix = 3647.163  # J/kg.K, heat capacity of mix at 80C

        # Solar thermal heater (STH) properties
        sth_length = math.sqrt(n) * 1.529  # m, length of STH
        sth_height = math.sqrt(n) * 1.019  # m, height of STH

        D_pipe = 22 / 1000  # m, diameter of pipe
        A_pipe = math.pi * (D_pipe / 2) ** 2  # m^2
        t_pipe = 3 / 1000  # m, thickness of pipe
        k_pipe = 45  # W/mK, thermal conductivity of steel
        L_pipe = n * (1.1 / 1000) / A_pipe
        surf_area_sth = sth_length * sth_height

        # Flow properties of water
        v_mix = (V_flow / 1000) / A_pipe  # m/s, velocity of water through radiator
        Re_d = (rho_mix * v_mix * D_pipe) / dyn_visc_mix  # Reynolds number of pipe

        # Laminar flow
        if Re_d <= 3000:
            Nu_D = 3.66  # Nusselt number using laminar correlation
        # Gnielinski Correlation
        elif 3000 <= Re_d < 5 * 10**6 and 0.5 <= Pr_mix <= 2000:
            f = (0.79 * math.log(Re_d) - 1.64) ** -2  # f value for Gnielinski correlation
            Nu_D = ((f / 8) * (Re_d - 1000) * Pr_mix) / (1 + (12.7 * (f / 8) * 0.5) * (Pr_mix * (2 / 3) - 1))
        # Dittus-Boelter Correlation
        elif Re_d >= 10000 and 0.6 <= Pr_mix <= 160:
            Nu_D = 0.023 * Re_d * (4 / 5) * Pr_mix * 0.3  # Nusselt number using Dittus-Boelter correlation

        h_mix = Nu_D * k_mix / D_pipe  # W/m^2K, convection heat transfer coefficient of water through pipe at 80C
        mass_flow_rate = v_mix * A_pipe * rho_mix  # kg/s, mass flow rate of water

        # Air convection coefficient
        rho_air = 1.293  # kg/m^3, density of air
        Pr_air = 0.7035  # Prandtl number for air
        k_air = 28.15 * 10 ** -3  # W/mK, thermal conductivity of air at 325K
        dyn_visc_air = 18.13 * 10 ** -6  # kg/m.s, dynamic viscosity of air

        Re_L_air = (rho_air * v_air * sth_length) / dyn_visc_air  # Reynolds number of pipe

        if Re_L_air <= 5 * 10**5:
            Nu_L_air = 0.664 * Re_L_air * 0.5 * Pr_air * (1 / 3)  # Nusselt number
        else:
            Nu_L_air = (0.037 * Re_L_air * (4 / 5) - 871) * Pr_air * (1 / 3)  # Nusselt number

        h_air = 3.3 * (k_air / sth_length) * Nu_L_air  # W/m^2K, convection heat transfer coefficient of air

        # Thermal resistance values
        R_water = 1 / (h_mix * math.pi * D_pipe * L_pipe)  # K/W, R value of water through pipe
        R_pipe = math.log(((D_pipe / 2) + t_pipe) / (D_pipe / 2)) / (2 * math.pi * k_pipe * L_pipe)  # K/W, R value of pipe
        R_air = 1 / (h_air * sth_height * sth_length * n)  # K/W, R value of water through pipe
        R_total = R_water + R_pipe + R_air  # K/W, total R value of radiator

        # Heat gain
        def cal_T_out(T_amb, T_in):
            return T_amb - math.exp(-1 / (mass_flow_rate * c_p_mix * R_total)) * (T_amb - T_in)

        T_out = cal_T_out(T_amb, T_in)

        Q_out = G * surf_area_sth * 0.521 - mass_flow_rate * c_p_mix * (T_in - T_out)

        T_out = Q_out / (mass_flow_rate * c_p_mix) + T_in

        return T_out, Q_out

    def input_water(self, litre: Length, temperature: Temperature) -> None:
        self.weight = self.density.calculate_mass(litre)
        self.temperature = temperature

    def output_water(self) -> (Weight, Temperature):
        temp = Weight(self.weight.value), Temperature(self.temperature.value)
        self.weight = Weight(0)
        self.temperature = Temperature.from_celsius(self.INITIAL_TEMPERATURE_C)
        return temp

    def add_water(self, litre: Length, temperature: Temperature) -> None:
        additional_water = self.density.calculate_mass(litre)
        additional_energy = self.shc.calculate_energy(temperature, additional_water)
        own_energy = self.shc.calculate_energy(self.temperature, self.weight)
        self.weight += additional_water
        self.temperature = self.shc.calculate_heat(own_energy + additional_energy, self.weight)

    def take_water(self, litre: Length) -> (Weight, Temperature):
        taken = self.density.calculate_mass(litre)
        self.weight -= taken
        if self.weight.value <= 0:
            raise AttributeError('Water cannot be taken that is not inside the water buffer.')
        return taken, Temperature(self.temperature.value)

    def print_statistics(self):
        print(f'{self.name} produced: {self.generation.format_watt_hours()}')
