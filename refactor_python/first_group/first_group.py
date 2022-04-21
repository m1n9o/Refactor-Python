
class Order:
    def __init__(self, price):
        self.basePrice = price


if __name__ == "__main__":
    anOrder = Order(10)
    print(anOrder.basePrice > 100)
