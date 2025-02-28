import aiohttp
from external_apis.common import TIMEOUT
from external_apis.orders.utils import map_order_details_to_model, map_order_to_model


def create_payload(order_id: int):
    return {
        "operationName": "OrderDetails",
        "variables": {
            "storeId": "4771",
            "orderId": order_id,
        },
        "query":
        "query OrderDetails($storeId: String!, $orderId: Int!) {\n  order(restaurantId: $storeId, id: $orderId) {\n    id\n    customerName\n    number\n    status\n    createdAt\n    deliveryStatus\n    submittedAt\n    driverId\n    updatingStatus {\n      orderGettingUpdated\n      nextStatus\n      __typename\n    }\n    deliveryType\n    paymentStatus\n    cancellationReason\n    voucherDiscountedItems {\n      menuItemId\n      titleEn\n      titleAr\n      totalPriceBeforeVoucher\n      voucherDiscount\n      totalPriceAfterVoucher\n      __typename\n    }\n    otherReason\n    beachUmbrella {\n      number\n      specialDirections\n      __typename\n    }\n    discountedAmount\n    paidByWallet\n    typeOfRefund\n    paidByCreditCard\n    refundedAmount\n    compensation {\n      percentage\n      amount\n      __typename\n    }\n    totalRefund\n    verdFees\n    engageFees\n    feastFees\n    branchId\n    branchData {\n      titleAr\n      titleEn\n      lat\n      lng\n      externalId\n      id\n      __typename\n    }\n    isScheduled\n    firingTime\n    timeSlot\n    expectedAt\n    orderItems {\n      id\n      menuItem {\n        id\n        titleEn\n        titleAr\n        photoUrl\n        variantPhotoUrl\n        variantsTitleAr\n        variantsTitleEn\n        maxPrepTime\n        __typename\n      }\n      imageUrl\n      notes\n      orderId\n      properties {\n        id\n        titleAr\n        titleEn\n        propertyValues {\n          id\n          titleAr\n          titleEn\n          price\n          quantity\n          isFree\n          __typename\n        }\n        __typename\n      }\n      quantity\n      totalAdditionalCharge\n      totalPrice\n      unitPrice\n      variant {\n        titleAr\n        titleEn\n        prepTime\n        price\n        discountedPrice\n        barCode\n        externalId\n        __typename\n      }\n      __typename\n    }\n    deliveryZone {\n      zoneName\n      __typename\n    }\n    userData {\n      address {\n        area {\n          titleAr\n          titleEn\n          lat\n          lng\n          cityTitleEn\n          cityTitleAr\n          __typename\n        }\n        building\n        street\n        floor\n        title\n        block\n        avenue\n        unitNo\n        unitType\n        notes\n        lat\n        lng\n        cityName\n        areaName\n        __typename\n      }\n      car {\n        make\n        model\n        color\n        licenseNumber\n        __typename\n      }\n      phoneNumber\n      email\n      name\n      recipient {\n        name\n        phoneNumber\n        giftNotes\n        __typename\n      }\n      __typename\n    }\n    stateHistories {\n      state\n      createdAt\n      userType\n      entityType\n      assignee\n      assigneeAr\n      actionBy\n      partnerError\n      __typename\n    }\n    total\n    deliveryFee\n    subtotal\n    subtotalAfterVoucher\n    tax\n    taxPercentage\n    taxInclusive\n    voucherAmount\n    voucherCode\n    paidThrough\n    refundTransactionsHistory {\n      refundId\n      updatedAt\n      status\n      __typename\n    }\n    deliveryCourierId\n    deliveryCourierName\n    deliveryCourier {\n      id\n      driverName\n      hasDriverInfo\n      driverPhoneNumber\n      driverAssigned\n      deliveryOrderStatus\n      isInternalDelivery\n      supportCancellation\n      courierId\n      courierDetails {\n        id\n        name\n        nameAr\n        country\n        description\n        supportNumber\n        businessId\n        businessName\n        displayNameAr\n        displayNameEn\n        __typename\n      }\n      driverMaxCapacity\n      trackingLink\n      referenceId\n      externalOrderIdentifierLink\n      externalOrderIdentifierType\n      __typename\n    }\n    paymentTransaction {\n      id\n      status\n      chargeId\n      paymentDate\n      __typename\n    }\n    deliveryTime\n    gift\n    inBetweenTransitions\n    partnerErrors\n    cashbackAmount\n    restaurantRiderBranchOrderData {\n      status\n      restaurantRider {\n        id\n        name\n        phoneNumber\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
    }


async def exec(zyda_cookie: str, order_id: int):
    url = "https://graphql-dash-wrapper.stellate.sh/graphql"
    headers = {
        "Authorization": f"Bearer {zyda_cookie}",
    }
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.post(url, headers=headers, json=create_payload(order_id)) as response:
            return await response.json()
