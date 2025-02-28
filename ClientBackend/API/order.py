from typing import List

from API.product import Product


class Order:
    def __init__(self, id, date, time, name, phone, pickupMethod, paymentMethod, zone, address, address_note, subtotal, delivery_fee, total, is_gift, gift_note=""):
        self.id = id
        self.date = date
        self.time = time
        self.name = name
        self.phone = phone
        self.pickupMethod = pickupMethod
        self.paymentMethod = paymentMethod
        self.zone = zone
        self.address = address
        self.address_note = address_note
        self.subtotal = subtotal
        self.deliveryFee = delivery_fee
        self.total = total
        self.is_gift = is_gift
        self.gift_note = gift_note
        self.products: List[Product] = []

    def __str__(self):
        return (
            f"Order(\n"
            f"  id={self.id}, type={type(self.id)}\n"
            f"  date={self.date}, type={type(self.date)}\n"
            f"  time={self.time}, type={type(self.time)}\n"
            f"  name={self.name}, type={type(self.name)}\n"
            f"  phone={self.phone}, type={type(self.phone)}\n"
            f"  pickupMethod={self.pickupMethod}, type={type(self.pickupMethod)}\n"
            f"  paymentMethod={self.paymentMethod}, type={type(self.paymentMethod)}\n"
            f"  zone={self.zone}, type={type(self.zone)}\n"
            f"  address={self.address}, type={type(self.address)}\n"
            f"  address_note={self.note}, type={type(self.note)}\n"
            f"  subtotal={self.subtotal}, type={type(self.subtotal)}\n"
            f"  delivery_fee={self.deliveryFee}, type={type(self.deliveryFee)}\n"
            f"  total={self.total}, type={type(self.total)}\n"
            f"  is_gift={self.is_gift}, type={type(self.is_gift)}\n"
            f"  gift_note={self.gift_note},  type={type(self.gift_note)}\n"
            f")"
        )
