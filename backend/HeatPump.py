from Appliance import Appliance


class HeatPump(Appliance):
    # https://en.wikipedia.org/wiki/Coefficient_of_performance
    name = 'HeatPump'

    def __init__(self, watts: float):
        super().__init__(watts)
