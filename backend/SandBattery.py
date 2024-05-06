from Physics import Energy, Length, Density, SpecificHeatCapacity, Temperature


class SandBattery:
    capacity = Energy.from_kilo_watt_hours(25000)
    length = Length(12)
    width = Length(12)
    height = Length(1)
    density = Density.from_predefined(Density.Predefined.SAND)
    efficiency = 1
    shc = SpecificHeatCapacity.from_predefined(SpecificHeatCapacity.Predefined.SAND)

    def __init__(self):
        volume = self.width * self.height * self.length
        mass = self.density.calculate_mass(volume)
        self.capacity = self.shc.calculate_energy((Temperature.from_celsius(500) - Temperature.from_celsius(20)), mass)
        # self.capacity.format_kilo_watt_hours()
