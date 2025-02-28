import requests
from datetime import datetime
import os
import asyncio
from core.models import Order
import external_apis
from time import time
from django.http import JsonResponse
from datetime import datetime, timedelta
from utils.BatchHandler import IncrementIterator, batch_request_handler
from dotenv import load_dotenv
load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL')


def print_orders(request):
    while True:
        time.sleep(60)
        today = datetime.today().date().isoformat()
        tommorow = (datetime.today().date() + timedelta(days=1)).isoformat()
        url = f'{BACKEND_URL}/api/store/orders/?created_at__gte={today}&expected_at__lt={tommorow}&branch_id=9700'
        response = requests.get(url)
        data = response.json()
        for order in data:
            Order.objects.get_or_create(id=order["id"], defaults={
                "number": order["number"],
                "created_at": order["created_at"],
                "expected_at": order["expected_at"],
            })

    return JsonResponse({"orders": data})
