email = "amremadel4@gmail.com"
password = "aeb15465943774cb"
ordersPayload = {
    "operationName": "Orders",
    "query":"query Orders($storeId: String!, $status: OrderStatus, $paymentStatuses: [OrderPaymentStatus], $paymentMethod: [PaymentMethod], $deliveryType: [DeliveryType], $isManualOrder: Boolean, $areas: [String], $branchId: String!, $submittedAt: [String], $phone: String, $number: String, $sort: OrderSorter, $statuses: [OrderStatus], $voucherCode: String, $deliveryZoneIn: [String], $searchValue: String, $searchCustomers: String, $paginateFrom: Int, $driverId: String) {\n  orders(\n    restaurantId: $storeId\n    status: $status\n    statuses: $statuses\n    paymentStatuses: $paymentStatuses\n    paginateFrom: $paginateFrom\n    searchValue: $searchValue\n    searchCustomers: $searchCustomers\n    filters: {branch_id: $branchId, submitted_at: $submittedAt, phone_number: [$phone], number: [$number], payment_methods: $paymentMethod, delivery_type: $deliveryType, is_manual_order: $isManualOrder, areas: $areas, voucher_code: $voucherCode, delivery_zone_in: $deliveryZoneIn, driver_id: $driverId}\n    sorter: $sort\n  ) {\n    orders {\n      id\n      number\n      isScheduled\n      expectedAt\n      firingTime\n      deliveryStatus\n      isManualOrder\n      rating\n      deliveryVatInclusive\n      customerName\n      deliveryZone {\n        zoneName\n        __typename\n      }\n      areaNameEn\n      areaNameAr\n      customerPhoneNumber\n      updatingStatus {\n        orderGettingUpdated\n        nextStatus\n        __typename\n      }\n      timeSlot\n      deliveryType\n      deliveryTime\n      driverId\n      branchName\n      branchId\n      paidThrough\n      status\n      paymentStatus\n      total\n      createdAt\n      closedAt\n      deliveryRating\n      submittedAt\n      deliveryCourierId\n      deliveryCourierName\n      gift\n      inBetweenTransitions\n      partnerErrors\n      cashbackAmount\n      __typename\n    }\n    totalCount\n    pastOrdersCount\n    currentOrdersCount\n    statusCount {\n      ready\n      dispatched\n      canceled\n      accepted\n      submitted\n      delivered\n      fulfilled\n      all\n      paid\n      paymentFailed\n      paymentExpired\n      waitingForPayment\n      redirectUrl\n      iframeUrl\n      __typename\n    }\n    __typename\n  }\n}",
    "variables":{
        "areas": [],
        "branchId": "",
        "deliveryType": [],
        "deliveryZoneIn": [],
        "driverId": "",
        "paginateFrom": 0,
        "paymentMethod": [],
        "sort": {
            "column": "created_at",
            "method": "desc"
        },
        "status": "current",
        "statuses": [],
        "storeId": "4771"
    }

}

loginPayload = {
    "operationName": "SignIn",
    "query": """
        mutation SignIn($email: String!, $password: String!) {
            signIn(email: $email, password: $password) {
                id
                name
                email
                phoneNumber
                accessToken
                createdAt
                __typename
            }
        }
    """,
    "variables": {
        "email": email,
        "password": password 
    }
}

def getOrderByIdPayload(orderId):
    orderByIdPayload = {
        "operationName": "OrderDetails",
        "query": "query OrderDetails($storeId: String!, $orderId: Int!) {  order(restaurantId: $storeId, id: $orderId) {\n    id\n    customerName\n    number\n    status\n    createdAt\n    deliveryStatus\n    submittedAt\n    driverId\n    updatingStatus {\n      orderGettingUpdated\n      nextStatus\n      __typename\n    }\n    deliveryType\n    paymentStatus\n    cancellationReason\n    voucherDiscountedItems {\n      menuItemId\n      titleEn\n      titleAr\n      totalPriceBeforeVoucher\n      voucherDiscount\n      totalPriceAfterVoucher\n      __typename\n    }\n    otherReason\n    beachUmbrella {\n      number\n      specialDirections\n      __typename\n    }\n    discountedAmount\n    paidByWallet\n    typeOfRefund\n    paidByCreditCard\n    refundedAmount\n    compensation {\n      percentage\n      amount\n      __typename\n    }\n    totalRefund\n    verdFees\n    engageFees\n    feastFees\n    branchId\n    branchData {\n      titleAr\n      titleEn\n      lat\n      lng\n      externalId\n      id\n      __typename\n    }\n    isScheduled\n    firingTime\n    timeSlot\n    expectedAt\n    orderItems {\n      id\n      menuItem {\n        id\n        titleEn\n        titleAr\n        photoUrl\n        variantPhotoUrl\n        variantsTitleAr\n        variantsTitleEn\n        maxPrepTime\n        __typename\n      }\n      imageUrl\n      notes\n      orderId\n      properties {\n        id\n        titleAr\n        titleEn\n        propertyValues {\n          id\n          titleAr\n          titleEn\n          price\n          quantity\n          isFree\n          __typename\n        }\n        __typename\n      }\n      quantity\n      totalAdditionalCharge\n      totalPrice\n      unitPrice\n      variant {\n        titleAr\n        titleEn\n        prepTime\n        price\n        discountedPrice\n        barCode\n        externalId\n        __typename\n      }\n      __typename\n    }\n    deliveryZone {\n      zoneName\n      __typename\n    }\n    userData {\n      address {\n        area {\n          titleAr\n          titleEn\n          lat\n          lng\n          cityTitleEn\n          cityTitleAr\n          __typename\n        }\n        building\n        street\n        floor\n        title\n        block\n        avenue\n        unitNo\n        unitType\n        notes\n        lat\n        lng\n        cityName\n        areaName\n        __typename\n      }\n      car {\n        make\n        model\n        color\n        licenseNumber\n        __typename\n      }\n      phoneNumber\n      email\n      name\n      recipient {\n        name\n        phoneNumber\n        giftNotes\n        __typename\n      }\n      __typename\n    }\n    stateHistories {\n      state\n      createdAt\n      userType\n      entityType\n      assignee\n      assigneeAr\n      actionBy\n      partnerError\n      __typename\n    }\n    total\n    deliveryFee\n    subtotal\n    subtotalAfterVoucher\n    tax\n    taxPercentage\n    taxInclusive\n    voucherAmount\n    voucherCode\n    paidThrough\n    refundTransactionsHistory {\n      refundId\n      updatedAt\n      status\n      __typename\n    }\n    deliveryCourierId\n    deliveryCourierName\n    deliveryCourier {\n      id\n      driverName\n      hasDriverInfo\n      driverPhoneNumber\n      driverAssigned\n      deliveryOrderStatus\n      isInternalDelivery\n      supportCancellation\n      courierId\n      courierDetails {\n        id\n        name\n        nameAr\n        country\n        description\n        supportNumber\n        businessId\n        businessName\n        displayNameAr\n        displayNameEn\n        __typename\n      }\n      driverMaxCapacity\n      trackingLink\n      referenceId\n      externalOrderIdentifierLink\n      externalOrderIdentifierType\n      __typename\n    }\n    paymentTransaction {\n      id\n      status\n      chargeId\n      paymentDate\n      __typename\n    }\n    deliveryTime\n    gift\n    inBetweenTransitions\n    partnerErrors\n    cashbackAmount\n    restaurantRiderBranchOrderData {\n      status\n      restaurantRider {\n        id\n        name\n        phoneNumber\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
        "variables":{
            "orderId": orderId,
            "storeId": "4771"
        }
    }
    return orderByIdPayload

def getOrderByNamePayload(orderName):
    ordersPayload = {
        "operationName": "Orders",
        "query":"query Orders($storeId: String!, $status: OrderStatus, $paymentStatuses: [OrderPaymentStatus], $paymentMethod: [PaymentMethod], $deliveryType: [DeliveryType], $isManualOrder: Boolean, $areas: [String], $branchId: String!, $submittedAt: [String], $phone: String, $number: String, $sort: OrderSorter, $statuses: [OrderStatus], $voucherCode: String, $deliveryZoneIn: [String], $searchValue: String, $searchCustomers: String, $paginateFrom: Int, $driverId: String) {\n  orders(\n    restaurantId: $storeId\n    status: $status\n    statuses: $statuses\n    paymentStatuses: $paymentStatuses\n    paginateFrom: $paginateFrom\n    searchValue: $searchValue\n    searchCustomers: $searchCustomers\n    filters: {branch_id: $branchId, submitted_at: $submittedAt, phone_number: [$phone], number: [$number], payment_methods: $paymentMethod, delivery_type: $deliveryType, is_manual_order: $isManualOrder, areas: $areas, voucher_code: $voucherCode, delivery_zone_in: $deliveryZoneIn, driver_id: $driverId}\n    sorter: $sort\n  ) {\n    orders {\n      id\n      number\n      isScheduled\n      expectedAt\n      firingTime\n      deliveryStatus\n      isManualOrder\n      rating\n      deliveryVatInclusive\n      customerName\n      deliveryZone {\n        zoneName\n        __typename\n      }\n      areaNameEn\n      areaNameAr\n      customerPhoneNumber\n      updatingStatus {\n        orderGettingUpdated\n        nextStatus\n        __typename\n      }\n      timeSlot\n      deliveryType\n      deliveryTime\n      driverId\n      branchName\n      branchId\n      paidThrough\n      status\n      paymentStatus\n      total\n      createdAt\n      closedAt\n      deliveryRating\n      submittedAt\n      deliveryCourierId\n      deliveryCourierName\n      gift\n      inBetweenTransitions\n      partnerErrors\n      cashbackAmount\n      __typename\n    }\n    totalCount\n    pastOrdersCount\n    currentOrdersCount\n    statusCount {\n      ready\n      dispatched\n      canceled\n      accepted\n      submitted\n      delivered\n      fulfilled\n      all\n      paid\n      paymentFailed\n      paymentExpired\n      waitingForPayment\n      redirectUrl\n      iframeUrl\n      __typename\n    }\n    __typename\n  }\n}",
        "variables":{
            "areas": [],
            "branchId": "",
            "deliveryType": [],
            "deliveryZoneIn": [],
            "driverId": "",
            "paginateFrom": 0,
            "paymentMethod": [],
            "searchValue": orderName,
            "sort": {
                "column": "created_at",
                "method": "desc"
            },
            "statuses": [],
            "storeId": "4771"
        }
    }
    return ordersPayload