import math

from Appliance import Appliance
from DebugLevel import DebugLevel
from Physics import Temperature, Power, Length, Time


class Radiator (Appliance):
    name = 'Radiator'
    should_activate = False

    flow_rate = Length.from_litre(0.015)
    litres = flow_rate * Time.from_minutes(10).value

    # Water properties
    rho_water = 1000 # 971.8  # kg/m^3, density of water at 80C
    dyn_visc = 0.000355  # Ns/m^2, dynamic viscosity of water at 80C
    k_water = 0.67  # W/mK, thermal conductivity of water at 80C
    Pr = 2.22  # Prandtl number at 80C
    c_p_water = 4180 # 4196.9  # J/kgK, heat capacity of water at 80C

    # Radiator properties
    D_pipe = 14 / 1000  # m, diameter of pipe
    A_pipe = math.pi * (D_pipe / 2) ** 2  # m^2
    t_pipe = 3 / 1000  # m, thickness of pipe
    height_radiator = 0.6  # m, height of radiator
    l_radiator = 1  # m, length of radiator
    d_spacing = 0.025  # m, spacing between tubes
    n_tubes = 2 * round(l_radiator / d_spacing)  # number of tubes, double panel
    k_pipe = 45  # W/mK, thermal conductivity of steel
    L_pipe = n_tubes * height_radiator

    # Natural convection coefficient
    T_surface = 70  # C, radiator surface temperature
    g = 9.81  # m/s^2, acceleration due to gravity
    beta = 1 / 350
    kin_visc_air = 18.405e-6  # m^2/s, kinematic viscosity of air
    alpha_air = 26.2e-6  # m^2/s, alpha of air
    Pr_air = 0.7035  # Prandtl number for air
    k_air = 28.15e-3  # W/mK, thermal conductivity of air at 325K

    h_air = 7.5  # W/m^2K, natural convection heat transfer coefficient of air

    def __init__(self):
        super().__init__(0)

    def getRadiatorData(self, T_in: Temperature, T_room: Temperature, V_flow: Length) -> (Temperature, Power):
        # Flow properties
        T_in = T_in.get_celsius()
        T_room = T_room.get_celsius()
        V_flow = V_flow.value * 1000
        v_water = (V_flow / 1000) / self.A_pipe  # m/s, velocity of water through radiator
        Re_d = (self.rho_water * v_water * self.D_pipe) / self.dyn_visc  # Reynolds number of pipe

        # Laminar
        if Re_d <= 3000:
            Nu_D = 3.66  # Nusselt number using laminar correlation
        # Gnielinski Correlation
        elif 3000 <= Re_d < 5 * 10 ** 6 and 0.5 <= self.Pr <= 2000:
            f = (0.79 * math.log(Re_d) - 1.64) ** -2  # f value for Gnielinski correlation
            Nu_D = (((f / 8) * (Re_d - 1000) * self.Pr) /
                    (1 + (12.7 * (f / 8) ** 0.5) * (self.Pr ** (2 / 3) - 1)))  # Nusselt number using Gnielinski correlation
        # Dittus-Boelter Correlation
        elif Re_d >= 10000 and 0.6 <= self.Pr <= 160:
            Nu_D = 0.023 * Re_d ** (4 / 5) * self.Pr ** 0.3  # Nusselt number using Dittus-Boelter correlation
        else:
            raise NotImplementedError('Radiator data not available')
        h_avg = Nu_D * self.k_water / self.D_pipe  # W/m^2K, convection heat transfer coefficient of water through pipe at 80C
        mass_flow_rate = v_water * self.A_pipe * self.rho_water  # kg/s, mass flow rate of water

        Ra_L = ((self.g * self.beta * abs(self.T_surface - T_room) * self.height_radiator ** 3) /
            (self.kin_visc_air * self.alpha_air))
        Nu_L = (0.825 + (0.387 * Ra_L ** (1 / 6)) / (1 + (0.492 / self.Pr_air) ** (9 / 16)) ** (8 / 27)) ** 2
        # Nu_L = 0.68 + (0.670 * Ra_L ** (1 / 4)) / (1 + (0.492 / Pr_air) ** (9 / 16)) ** (4 / 9)
        # h_air = (k_air / height_radiator) * Nu_L

        # Thermal resistance values
        R_water = 1 / (h_avg * math.pi * self.D_pipe * self.L_pipe)  # K/W, R value of water through pipe
        R_pipe = math.log((self.D_pipe / 2 + self.t_pipe) / (self.D_pipe / 2)) / (2 * math.pi * self.k_pipe * self.L_pipe)  # K/W, R value of pipe
        R_air = 1 / (self.h_air * math.pi * (self.D_pipe + 2 * self.t_pipe) * self.L_pipe)  # K/W, R value of water through pipe
        R_total = R_water + R_pipe + R_air  # m^2K/W, total R value of radiator

        def cal_T_out(T_room, T_in):
            return T_room - math.exp(-1 / (mass_flow_rate * self.c_p_water * R_total)) * (T_room - T_in)

        T_out = cal_T_out(T_room, T_in)

        # del_T_log_mean = ((T_room - T_in) - (T_room - T_out)) / np.log((T_room - T_out) / (T_room - T_in))
        # Q_out = del_T_log_mean / R_total

        Q_out = mass_flow_rate * self.c_p_water * (T_in - T_out)

        return Temperature.from_celsius(T_out), Power(Q_out)

    def set_flow_rate(self, flow_rate):
        self.flow_rate = flow_rate
        self.litres = flow_rate * Time.from_minutes(10).value

    def step(self, t: int, absolute_step: int, verbosity: DebugLevel = DebugLevel.INFORMATIONAL):
        self.on = self.should_activate

    def heat(self):
        pass

    def activate(self):
        self.should_activate = True

    def deactivate(self):
        self.should_activate = False
