from Appliance import Appliance


class HeatPump(Appliance):
    name = 'HeatPump'

    def __init__(self, watts: float):
        super().__init__(watts)
