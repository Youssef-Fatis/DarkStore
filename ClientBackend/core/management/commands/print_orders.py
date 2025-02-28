import os
import time
import asyncio
import logging
import pprint
from time import sleep
from datetime import datetime, timedelta

import requests
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import transaction
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

# External API and utility imports
from API.zyda_order_service import ZydaOrderService
from API.order_zyda_model import ZydasOrder
import external_apis
from utils.batch_handler import ArrayIterator, IncrementIterator, batch_request_handler
from utils.date_functions import convert_iso_to_date, get_date_range_one_week_eariler_from_today

# Adjust the import to your Order model location
from core.models import Order

# Load environment variables
load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def save_order_in_db(order, order_id):
    """
    Save the order in the database using an atomic transaction.
    """
    order = order['data']['order']
    try:
        with transaction.atomic():
            obj, created = Order.objects.get_or_create(
                id=order_id,
                defaults={
                    "number": order["number"],
                    "created_at": order["createdAt"],
                    "expected_at": order["expectedAt"],
                }
            )
            if created:
                logger.info(f"Order {order['id']} saved to DB.")
            else:
                logger.info(f"Order {order['id']} already exists in DB.")
    except Exception as e:
        logger.error(f"Error saving order {order['id']} in DB: {e}")
        raise


zydaOrderService = ZydaOrderService()


async def print_and_save_orders(token: str, orders_tuple):
    """
    Asynchronously fetch order details, print and save them.
    """

    async def fetch_data(order_tuple):
        main_id, reference_id = order_tuple
        try:
            logger.info(f"Fetching details for order ID: {reference_id}")
            order = await external_apis.orders.get_order_details.exec(token, reference_id)
            logger.info(
                f"Successfully fetched details for order ID: {reference_id}")

            newOrder = ZydasOrder.zydasOrderFactory(order, zydaOrderService)
            logger.info(f"Created ZydasOrder for order: {newOrder.orderName}")

            zydaOrderService.createReciptForOrder(newOrder)
            logger.info(f"Created receipt for order: {newOrder.orderName}")

            zydaOrderService.printOrderReceipt(newOrder.orderName)
            logger.info(f"Printed receipt for order: {newOrder.orderName}")

            await sync_to_async(save_order_in_db)(order, main_id)
            logger.info(f"Order {reference_id} processed and saved.")
        except Exception as e:
            logger.error(f"Error processing order {reference_id}: {e}")

    logger.info("Starting batch processing of orders.")
    result = await batch_request_handler(
        5,
        ArrayIterator(orders_tuple),
        fetch_data
    )
    logger.info("Finished batch processing of orders.")
    return result


class Command(BaseCommand):
    help = "Fetch and process orders indefinitely"

    def handle(self, *args, **options):
        logger.info("Starting to fetch orders indefinitely...")
        dates = [datetime.today() - timedelta(days=1),
                 datetime.today(), datetime.today() + timedelta(days=1)]
        while True:
            try:
                for i, date in enumerate(dates):
                    print(f"{i + 1}. {date.date()}")

                index = int(input("Please Select Date: ")) - 1
                if index < 0:
                    raise IndexError("Enter valid index")
                selected_date = dates[index]
                break
            except:
                print("Enter valid date")
        print(f"Selected Date is {selected_date.date()}")
        while True:
            # Calculate the date range for the query
            today = (selected_date.date() +
                     timedelta(hours=10)).isoformat()
            tomorrow = (selected_date.date() +
                        timedelta(days=1, hours=5)).isoformat()
            logger.info(
                f"Fetching orders for date range: {today} to {tomorrow}")

            # Construct the URL for the API call
            url = f"{BACKEND_URL}/api/store/orders/?expected_at__gte={today}&expected_at__lt={tomorrow}&branch_id={os.getenv("BRANCH_ID")}"
            logger.info(f"Requesting orders from URL: {url}")

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise error for bad status codes
                data = response.json()
                logger.info(f"Fetched {len(data)} orders from the API.")
            except requests.RequestException as e:
                logger.error(f"Error fetching orders: {e}")
                sleep(60)
                continue

            # Log the fetched data at debug level
            logger.debug(f"Fetched data: {pprint.pformat(data)}")

            # Retrieve existing order IDs from the database
            orders_in_db = Order.objects.filter().values_list('id', flat=True)
            orders_in_db = list(orders_in_db)
            logger.info(f"Found {len(orders_in_db)} orders already in DB.")

            # Filter out orders that already exist in the database
            filtered_data = [
                (order["id"], order['reference_id']) for order in data if order['id'] not in orders_in_db
            ]
            logger.info(
                f"{len(filtered_data)} new orders to process after filtering.")

            if filtered_data:
                try:
                    token = external_apis.auth.utils.get_token(
                        os.getenv("EMAIL"), os.getenv("PASSWORD")
                    )
                    logger.info("Obtained authentication token.")
                    asyncio.run(print_and_save_orders(token, filtered_data))
                except Exception as e:
                    logger.error(f"Error during asynchronous processing: {e}")
            else:
                logger.info("No new orders to process.")

            logger.info("Sleeping for 60 seconds before next fetch...")
            sleep(60)
