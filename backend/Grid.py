from DebugLevel import DebugLevel


class Grid(object):
    buy_price = 9.528 * (1/100) * (1/1000)  # 9,528ct/kWh  # 0.25
    sell_price = buy_price / 4  # 0.10

    def __init__(self):
        self.bought = 0
        self.sold = 0

    def __str__(self):
        return 'Grid'

    def buy(self, energy: float):
        if energy < 0:
            raise ValueError("Energy")
        self.bought += energy
        return self.buy_price * energy

    def sell(self, energy: float):
        if energy < 0:
            raise ValueError("Energy")
        self.sold += energy
        return self.sell_price * energy

    def print_statistics(self, verbosity=DebugLevel.INFORMATIONAL):
        diff = self.bought - self.sold
        diff_money = self.bought * self.buy_price - self.sold * self.sell_price
        if verbosity >= DebugLevel.DEBUGGING:
            print(f'Bought: {round(self.bought, 2)}W for {round(self.bought * self.buy_price, 2)}€')
            print(f'Sold: {round(self.sold, 2)}W for {round(self.sold * self.sell_price, 2)}€')
            print(f'Diff: {round(diff, 2)}W for {round(diff_money, 2)}€')
        if verbosity >= DebugLevel.INFORMATIONAL:
            print(f'Bought: {round(self.bought / 1000, 2)}kWh for {round(self.bought * self.buy_price, 2)}€')
            print(f'Sold: {round(self.sold / 1000, 2)}kWh for {round(self.sold * self.sell_price, 2)}€')
            print(f'Diff: {round(diff / 1000, 2)}kWh for {round(diff_money, 2)}€')
