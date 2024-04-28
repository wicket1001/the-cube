from DebugLevel import DebugLevel
from Physics import Energy, Money


class Grid(object):
    buy_price = Money.from_cent(9.528)  # 9,528ct/kWh  # 0.25
    sell_price = buy_price / 4  # 0.10

    def __init__(self):
        self.bought = Energy(0)
        self.sold = Energy(0)
        self.buying = Energy(0)
        self.selling = Energy(0)

    def __str__(self):
        return 'Grid'

    def buy(self, energy: Energy) -> Money:
        if energy < Energy(0):
            raise ValueError("Energy")
        self.buying = energy
        self.bought += energy
        return self.buy_price.calculate_kWh_cost(energy)

    def sell(self, energy: Energy) -> Money:
        if energy < Energy(0):
            raise ValueError("Energy")
        self.selling = energy
        self.sold += energy
        return self.sell_price.calculate_kWh_cost(energy)

    def print_statistics(self, verbosity=DebugLevel.INFORMATIONAL):
        diff = self.bought - self.sold
        diff_money = self.buy_price.calculate_kWh_cost(self.bought) - self.sell_price.calculate_kWh_cost(self.sold)
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'Bought: {self.bought} for {self.buy_price.calculate_kWh_cost(self.bought)}')
            print(f'Sold: {self.sold} for {self.sell_price.calculate_kWh_cost(self.sold)}')
            print(f'Diff: {diff} for {diff_money}')
        if verbosity >= DebugLevel.INFORMATIONAL:
            print(f'Bought: {self.bought.format_kilo_watt_hours()} for {self.buy_price.calculate_kWh_cost(self.bought)}')
            print(f'Sold: {self.sold.format_kilo_watt_hours()} for {self.sell_price.calculate_kWh_cost(self.sold)}')
            print(f'Diff: {diff.format_kilo_watt_hours()} for {diff_money}')

    def reset(self):
        self.buying = Energy(0)
        self.selling = Energy(0)
