
class Grid(object):
    sell_price = 0.10
    buy_price = 0.25

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

    def print_statistics(self):
        diff = self.bought - self.sold
        diff_money = self.bought * self.buy_price - self.sold * self.sell_price
        print(f'Bought: {round(self.bought, 2)} for {round(self.bought * self.buy_price, 2)}')
        print(f'Sold: {round(self.sold, 2)} for {round(self.sold * self.sell_price, 2)}')
        print(f'Diff: {round(diff, 2)} for {round(diff_money, 2)}')
