import math


class SolarPanel:
    # 52MW
    # 26/15 MW pro Tag
    # 576m^2 Solarpanel
    # 0.003009 MW pro Panel pro Tag
    # 3009 W pro Panel pro Tag
    TO_WATT_HOURS = 6
    SOLAR_EFFICIENCY = 0.2
    JOULE_TO_WATT_HOUR = 1 / 3600
    JOULE_TO_KWH = JOULE_TO_WATT_HOUR * (1 / 1000)
    # JOULE_TO_KWH = 0.000000278
    solar_panel_efficiency = SOLAR_EFFICIENCY * JOULE_TO_WATT_HOUR
    SECONDS_TO_10_MIN = 600

    production = 0
    watt_sum = 0
    iterations = 0
    radiations = []
    area = 1

    def __str__(self):
        return "SolarPanel"

    def save_weather(self, array):
        self.radiations = array

    def step(self, t: int, absolute_step: int) -> float:
        if len(self.radiations) == 0:
            # return int(math.sin(t) * 1000)
            energy_production = math.sin(t / (144/3)) * 100
            energy_production *= self.area
            self.production += energy_production
            return round(energy_production, 2)
        else:
            # print(absolute_step)
            energy_production = 0
            radiation = self.radiations[absolute_step]
            self.iterations += 1
            # print('Rad', radiation)

            watt = radiation * self.area
            # print('WATT', watt)
            joule_per_10min = watt * self.SECONDS_TO_10_MIN
            # print('Joule', joule_per_10min)

            factor = math.sin(t / (144/3))
            # print('Time factor', factor)
            effective_watt = watt * factor
            effective_joule = joule_per_10min * factor
            # print('Effective Joule', effective_joule)

            energy_production = joule_per_10min * self.solar_panel_efficiency # TODO effective_joule
            # print('Energy production', energy_production)

            self.watt_sum += watt
            self.production += energy_production
            return energy_production

    def print_statistics(self):
        print(f'Produced: {round(self.production, 2)}Wh')
        if self.iterations == 144:
            # print(f'-- Watt Sum: {self.watt_sum}')
            avg_watt = self.watt_sum / self.iterations
            # print(f'Watt Average: {avg_watt}')
            watt_second = avg_watt * self.solar_panel_efficiency
            # print(f'Watt seconds: {watt_second}')
            watt_per_day = watt_second * 24 * 3600
            print(f'watt_per_day: {round(watt_per_day, 2)}Wh')
