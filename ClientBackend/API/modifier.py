class Modifier:
    def __init__(self, name, quantity, price) -> None:
        self.name = name
        self.quantity = quantity
        self.price = price

    def __str__(self) -> str:
        return f"Modifier(name='{self.name}', quantity={self.quantity}, price={self.price:.2f})"
