def map_order_to_model(order):
    zone = order['deliveryZone'].get(
        'zoneName') if order.get('deliveryZone') else None
    return {
        "reference_id": order.get('id'),
        "number": order.get('number'),
        "created_at": order.get('createdAt'),
        "expected_at": order.get('expectedAt'),
        "delivery_type": order.get('deliveryType'),
        "branch_id": order.get('branchId'),
        "zone": zone,
        "total": order.get('total'),
        "paid_through": order.get('paidThrough'),
        "customer": {
            "name": order.get('customerName'),
            "phone_number": order.get('customerPhoneNumber')
        },
    }


def map_order_details_to_model(order):
    user_data = order['userData']
    customer = {
        "name": user_data["name"],
        "phone_number": user_data["phoneNumber"],
        "email": user_data["email"]
    }

    recipient_data = user_data['recipient']
    recipient = None
    gift = None
    if recipient_data:
        recipient = {
            "name": recipient_data["name"],
            "phone_number": recipient_data["phoneNumber"],
        }
        gift = {
            "recipient": recipient,
            "gift_note": recipient_data["giftNotes"]
        }

    user_address = user_data["address"]
    address = None
    if user_address:
        address = {
            "zone": order['deliveryZone'].get('zoneName', None),
            "area": user_address["area"],
            "building": user_address["building"],
            "street": user_address["street"],
            "floor": user_address["floor"],
            "title": user_address["title"],
            "block": user_address["block"],
            "avenue": user_address["avenue"],
            "unitNo": user_address["unitNo"],
            "unit_type": user_address["unitType"],
            "notes": user_address["notes"],
            "lat": user_address["lat"],
            "lng": user_address["lng"],
            "city_name": user_address["cityName"],
            "area_name": user_address["areaName"],
        }
    transaction = {
        "discounted_amount": order.get("discountedAmount"),
        "paid_by_wallet": order.get("paidByWallet"),
        "paid_by_credit_card": order.get("paidByCreditCard"),
        "refunded_amount": order.get("refundedAmount"),
        "total_refund": order.get("totalRefund"),
        "total": order.get("total"),
        "delivery_fee": order.get("deliveryFee"),
        "subtotal": order.get("subtotal"),
        "subtotal_after_voucher": order.get("subtotalAfterVoucher"),
        "paid_through": order.get("paidThrough"),
        "tax": order.get("tax"),
        "tax_percentage": order.get("taxPercentage"),
        "tax_inclusive": order.get("taxInclusive"),
        "voucher_amount": order.get("voucherAmount"),
        "voucher_code": order.get("voucherCode"),
    }
    return {
        "reference_id": order.get('id'),
        "number": order.get('number'),
        "created_at": order.get('createdAt'),
        "expected_at": order.get('expectedAt'),
        "delivery_type": order.get('deliveryType'),
        "branch_id": order.get('branchId'),
        "customer": customer,
        "gift": gift,
        "address": address,
        "transaction": transaction,
    }
