from typing import List
from API.product import Product


class ZydasOrder:
    def __init__(self, id, orderName, customerName, createdAt, deliveryType, discountedAmount, address, addressNote, areaName, lat, long, phoneNumber, total, deliveryFee,  subtotal, subtotalAfterVoucher, voucherAmount, paidThrough, gift=False, recipientName="", recipientPhoneNumber="", giftNotes="", products=None):
        self.id = id
        self.orderName = orderName
        self.customerName = customerName
        self.createdAt = createdAt
        self.deliveryType = deliveryType
        self.discountedAmount = discountedAmount
        self.addressNote = addressNote
        self.address = address
        self.areaName = areaName
        self.lat = lat
        self.long = long
        self.phoneNumber = phoneNumber
        self.total = total
        self.deliveryFee = deliveryFee
        self.subtotal = subtotal
        self.subtotalAfterVoucher = subtotalAfterVoucher
        self.voucherAmount = voucherAmount
        self.paidThrough = paidThrough
        self.gift = gift
        self.recipientName = recipientName
        self.recipientPhoneNumber = recipientPhoneNumber
        self.giftNotes = giftNotes
        self.products: List[Product] = products if products is not None else []

    def zydasOrderFactory(order, zydaOrderService):
        orderDetails = order
        # Use `.get()` with default values to handle missing or None values
        id = orderDetails.get("id", "")
        orderName = orderDetails.get("number", "")
        customerName = orderDetails.get("customerName", "")
        createdAt = orderDetails.get("submittedAt", "")
        deliveryType = orderDetails.get("deliveryType", "")
        discountedAmount = orderDetails.get("discountedAmount", "")

        userData = orderDetails.get("userData", {})
        address = userData.get("address", {})
        # Safeguard against None or non-dictionary address
        if not isinstance(address, dict):
            address = {}
        building = address.get("building", "")
        street = address.get("street", "")
        floor = address.get("floor", "")
        title = address.get("title", "")
        block = address.get("block", "")
        avenue = address.get("avenue", "")
        unitNo = address.get("unitNo", "")
        lat = address.get("lat", "")
        lng = address.get("lng", "")
        cityName = address.get("cityName", "")
        areaName = address.get("areaName", "")

        fulladdress = (
            f"شقه رقم {unitNo} , الحى {block} , الدور {floor} , شارع {street} , عماره {building}  ."
        )
        addressNote = address.get("notes", "")
        phoneNumber = userData.get("phoneNumber", "")
        total = orderDetails.get("total", "")
        deliveryFee = orderDetails.get("deliveryFee", "")
        subtotal = orderDetails.get("subtotal", "")
        subtotalAfterVoucher = orderDetails.get("subtotalAfterVoucher", "")
        voucherAmount = orderDetails.get("voucherAmount", "")
        paidThrough = orderDetails.get("paidThrough", "")
        gift = orderDetails.get("gift", False)

        # Safely handle recipient data
        recipient = userData.get("recipient")
        recipientName = recipient.get("name", "") if recipient else ""
        recipientPhoneNumber = recipient.get(
            "phoneNumber", "") if recipient else ""
        recipientGiftNotes = recipient.get(
            "giftNotes", "") if recipient else ""
        products = zydaOrderService.creatingOrderProducts(orderDetails)
        zydaOrder = ZydasOrder(id, orderName, customerName, createdAt, deliveryType, discountedAmount,
                               fulladdress, addressNote, areaName, lat, lng, phoneNumber, total, deliveryFee, subtotal,
                               subtotalAfterVoucher, voucherAmount, paidThrough, gift, recipientName,
                               recipientPhoneNumber, recipientGiftNotes, products)
        return zydaOrder

    def __str__(self) -> str:
        products_str = ", ".join(str(product) for product in self.products)
        return (f"ZydasOrder(id={self.id}, orderName='{self.orderName}', customerName='{self.customerName}', "
                f"createdAt='{self.createdAt}', deliveryType='{self.deliveryType}', discountedAmount={self.discountedAmount:.2f}, "
                f"address='{self.address}', areaName='{self.areaName}', lat={self.lat}, long={self.long}, "
                f"phoneNumber='{self.phoneNumber}', total={self.total:.2f}, deliveryFee={self.deliveryFee:.2f}, "
                f"subtotal={self.subtotal:.2f}, subtotalAfterVoucher={self.subtotalAfterVoucher:.2f}, "
                f"voucherAmount={self.voucherAmount:.2f}, paidThrough='{self.paidThrough}', gift={self.gift}, "
                f"recipientName='{self.recipientName}', recipientPhoneNumber='{self.recipientPhoneNumber}', "
                f"giftNotes='{self.giftNotes}', products=[{products_str}])")
