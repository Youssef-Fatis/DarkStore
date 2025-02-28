import aiohttp
from external_apis.common import TIMEOUT
from external_apis.orders.utils import map_order_to_model


def create_payload(start: str, end: str, from_param: int):
    return {
        "operationName": "Orders",
        "variables": {
            "status": None,
            "paymentMethod": [],
            "deliveryType": [],
            "areas": [],
            "deliveryZoneIn": [],
            "driverId": "",
            "storeId": "4771",
            "branchId": "",
            "submittedAt": [start, end],
            "sort": {
                "method": "desc",
                "column": "created_at",
            },
            "paginateFrom": from_param,
            "statuses": [
                "submitted", "accepted", "ready", "dispatched", "delivered", "fulfilled"
            ],
        },
        "query": """
        query Orders($storeId: String!, $status: OrderStatus, $paymentStatuses: [OrderPaymentStatus], $paymentMethod: [PaymentMethod], $deliveryType: [DeliveryType], $isManualOrder: Boolean, $areas: [String], $branchId: String!, $submittedAt: [String], $phone: String, $number: String, $sort: OrderSorter, $statuses: [OrderStatus], $voucherCode: String, $deliveryZoneIn: [String], $searchValue: String, $searchCustomers: String, $paginateFrom: Int, $driverId: String) {
            orders(
                restaurantId: $storeId
                status: $status
                statuses: $statuses
                paymentStatuses: $paymentStatuses
                paginateFrom: $paginateFrom
                searchValue: $searchValue
                searchCustomers: $searchCustomers
                filters: {branch_id: $branchId, submitted_at: $submittedAt, phone_number: [$phone], number: [$number], payment_methods: $paymentMethod, delivery_type: $deliveryType, is_manual_order: $isManualOrder, areas: $areas, voucher_code: $voucherCode, delivery_zone_in: $deliveryZoneIn, driver_id: $driverId}
                sorter: $sort
            ) {
                orders {
                    id, number, isScheduled, expectedAt, firingTime, deliveryStatus, isManualOrder,
                    rating, deliveryVatInclusive, customerName, deliveryZone { zoneName __typename },
                    areaNameEn, areaNameAr, customerPhoneNumber, updatingStatus {
                        orderGettingUpdated, nextStatus, __typename
                    }, timeSlot, deliveryType, deliveryTime, driverId, branchName, branchId,
                    paidThrough, status, paymentStatus, total, createdAt, closedAt,
                    deliveryRating, submittedAt, deliveryCourierId, deliveryCourierName,
                    gift, inBetweenTransitions, partnerErrors, cashbackAmount, __typename
                },
                totalCount, pastOrdersCount, currentOrdersCount, statusCount {
                    ready, dispatched, canceled, accepted, submitted, delivered, fulfilled,
                    all, paid, paymentFailed, paymentExpired, waitingForPayment,
                    redirectUrl, iframeUrl, __typename
                }, __typename
            }
        }"""
    }


async def exec(zyda_cookie: str, start: str, end: str, from_param: int = 0):
    url = "https://graphql-dash-wrapper.stellate.sh/graphql"
    headers = {
        "Authorization": f"Bearer {zyda_cookie}",
    }
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.post(url, headers=headers, json=create_payload(start, end, from_param)) as response:
            response = await response.json()
            return [map_order_to_model(order) for order in response.get('data', {}).get('orders', {}).get('orders', [])]
