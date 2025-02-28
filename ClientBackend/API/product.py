from typing import List
from API.variant import Variant


class Product:
    def __init__(self, name, quantity, price, note):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.note = note
        self.variants: List[Variant] = []

    def __str__(self) -> str:
        variants_str = ", ".join(str(variant) for variant in self.variants)
        return (f"Product(name='{self.name}', quantity={self.quantity}, "
                f"price={self.price:.2f}, note='{self.note}', variants=[{variants_str}])")
