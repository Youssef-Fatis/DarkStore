import base64
from datetime import datetime, timezone
import os
import subprocess
import win32api
import win32print
import shutil
import sqlite3
import PyPDF2
import jinja2
import pandas as pd
import pdfkit
import pytz
from tqdm import tqdm
from API.order_zyda_model import ZydasOrder
from API.product import Product
from API.variant import Variant
from API.modifier import Modifier
reciept_template_path = './templates/reciept.html'
template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)
reciept_template = template_env.get_template(reciept_template_path)
config = pdfkit.configuration(wkhtmltopdf='./wkhtmltopdf.exe')
cairo_zone = pytz.timezone("Africa/Cairo")
manifesto_template_path = './templates/manifesto.html'
manifesto_template = template_env.get_template(manifesto_template_path)
base_dir = os.path.dirname(os.path.abspath(__file__))


def image_file_path_to_base64_string(filepath: str) -> str:
    '''
    Takes a filepath and converts the image saved there to its base64 encoding,
    then decodes that into a string.
    '''
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode()


image = image_file_path_to_base64_string('./templates/logo.png')


class ZydaOrderService:
    def insert_order(self, order: ZydasOrder, db_path):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # SQL query to insert data into ZydasOrder table
        query = '''
        INSERT INTO ZydasOrder (
            id, orderName, customerName, createdAt, deliveryType, discountedAmount,
            address, areaName, lat, long, phoneNumber, total, deliveryFee, 
            subtotal, subtotalAfterVoucher, voucherAmount, paidThrough, gift, 
            recipientName, recipientPhoneNumber, giftNotes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        gift = order.gift if order.gift is not None else False
        # Execute the query with the data from the order object
        cursor.execute(query, (
            order.id,
            order.orderName,
            order.customerName,
            order.createdAt,
            order.deliveryType,
            order.discountedAmount,
            order.address,
            order.areaName,
            order.lat,
            order.long,
            order.phoneNumber,
            order.total,
            order.deliveryFee,
            order.subtotal,
            order.subtotalAfterVoucher,
            order.voucherAmount,
            order.paidThrough,
            int(gift),
            order.recipientName,
            order.recipientPhoneNumber,
            order.giftNotes
        ))
        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
        print(f"Order {order.id} inserted successfully.")

    def fetch_all_order_ids(self, db_path):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to fetch all order IDs
        query = 'SELECT orderName FROM ZydasOrder;'

        # Execute the query and fetch all results
        cursor.execute(query)
        rows = cursor.fetchall()

        # Close the connection
        conn.close()

        # Extract IDs from the rows and return as a list
        order_ids = [row[0] for row in rows]
        return order_ids

    def creatingOrderProducts(self, order):
        products = []
        for item in order["orderItems"]:
            itemName = item["menuItem"]["titleEn"]
            itemQuantity = item["quantity"]
            itemTotalPrice = item["totalPrice"]
            itemNote = item["notes"]
            product = Product(itemName, itemQuantity, itemTotalPrice, itemNote)
            if 'properties' in item:
                for property in item["properties"]:
                    variantName = property["titleEn"]
                    variant = Variant(variantName)
                    for propertyValue in property["propertyValues"]:
                        propertyValueName = propertyValue["titleEn"]
                        propertyValueQuantity = propertyValue["quantity"]
                        propertyValuePrice = propertyValue["price"]
                        modifier = Modifier(
                            propertyValueName, propertyValueQuantity, propertyValuePrice)
                        variant.modifiers.append(modifier)
                    product.variants.append(variant)
            products.append(product)
        return products

    def createReciptForOrder(self, order: ZydasOrder):
        zone_directory_path = f"./output/{order.orderName}"
        pricing_list = {}
        pricing_list["Subtotal"] = order.subtotal
        if order.subtotal != order.subtotalAfterVoucher:
            pricing_list["Subtotal After Voucher"] = order.subtotalAfterVoucher
            pricing_list["Discounted Amount"] = order.discountedAmount
            pricing_list["Voucher Amount"] = order.voucherAmount
        pricing_list["Delivery Fee"] = order.deliveryFee
        if os.path.exists(zone_directory_path):
            shutil.rmtree(zone_directory_path)
        os.makedirs(zone_directory_path)
        # Parse the timestamp into a datetime object (in UTC)
        dt_utc = datetime.strptime(order.createdAt, "%Y-%m-%dT%H:%M:%S.%fZ")
        utc_zone = pytz.utc
        dt_utc = utc_zone.localize(dt_utc)
        dt_cairo = dt_utc.astimezone(cairo_zone)
        time = dt_cairo.strftime("%H:%M")
        date = dt_cairo.strftime("%d %b %Y")
        reciept_context = {'order': order,
                           'date': date,
                           'img_string': image,
                           'pricing_list': pricing_list
                           }
        reciept_text = reciept_template.render(reciept_context)
        reciept_pdf = f'{zone_directory_path}/{order.orderName}.pdf'
        pdfkit.from_string(reciept_text, reciept_pdf,
                           configuration=config, css='./templates/reciept.css',   options={
                               'encoding': 'UTF-8',
                               'no-pdf-compression': '',
                               'disable-smart-shrinking': '',
                           })

    def printOrderReceipt(self, orderId):
        # Relative file path
        file_path = f".\\output\\{orderId}\\{orderId}.pdf"
        print(file_path)

        # Get the default printer
        printer_name = win32print.GetDefaultPrinter()
        print(printer_name)

        # Send the print job directly to the printer
        win32api.ShellExecute(0, "print", file_path, None, ".", 0)

    def createCombinedRecipts(self, zone_number, orders_objects, courier, courier_pdfs_paths):
        zone_directory_path = f"./output/Zone {zone_number}"

        if os.path.exists(zone_directory_path):
            shutil.rmtree(zone_directory_path)
        os.makedirs(zone_directory_path)
        today = datetime.today()
        manifesto_bar = tqdm(total=1, desc=f"Creating Zone {
                             zone_number} Manifesto", unit="PDF")
        manifesto_context = {'orders': orders_objects,
                             'zone_number': zone_number,
                             'courier': courier,
                             'date': today.strftime("%d %b, %Y")}
        manifesto_pdf = f'{zone_directory_path}/manifesto.pdf'
        manifesto_text = manifesto_template.render(manifesto_context)
        manifesto_bar.update(1)
        manifesto_bar.close()
        courier_pdfs_paths.append([manifesto_pdf, [], zone_directory_path])
        pdfkit.from_string(manifesto_text, manifesto_pdf,
                           configuration=config, css='./templates/manifesto.css', options={'encoding': 'UTF-8', 'orientation': 'Landscape'})
        zone_bar = tqdm(total=len(orders_objects), desc=f"Creating Zone {
                        zone_number} Recipts", unit="PDF")
        for i, o in enumerate(orders_objects):
            pricing_list = {}
            pricing_list["Subtotal"] = o.subtotal
            if o.subtotal != o.subtotalAfterVoucher:
                pricing_list["Subtotal After Voucher"] = o.subtotalAfterVoucher
                pricing_list["Discounted Amount"] = o.discountedAmount
                pricing_list["Voucher Amount"] = o.voucherAmount
            pricing_list["Delivery Fee"] = o.deliveryFee
            reciept_context = {'order': o,
                               'zone_number': zone_number,
                               'courier': courier,
                               'date': today.strftime("%d %b, %Y"),
                               'pricing_list': pricing_list,
                               'img_string': image}
            reciept_text = reciept_template.render(reciept_context)
            reciept_pdf = f'{zone_directory_path}/{i+1}.pdf'
            courier_pdfs_paths[-1][1].append(reciept_pdf)
            pdfkit.from_string(reciept_text, reciept_pdf,
                               configuration=config, css='./templates/reciept.css',   options={
                                   'encoding': 'UTF-8',
                                   'no-pdf-compression': '',
                                   'disable-smart-shrinking': '',
                               })
            zone_bar.update(1)
        zone_bar.close()
        merger_bar = tqdm(total=len(orders_objects), desc=f"Merging Zone {
                          zone_number} Recipts into 1 pdf", unit="PDF")
        merger = PyPDF2.PdfMerger()
        merger.append(courier_pdfs_paths[-1][0])
        for pdf in courier_pdfs_paths[-1][1]:
            merger.append(pdf)
            merger_bar.update(1)
        merger.write(f"{courier_pdfs_paths[-1][2]}/combined.pdf")
        merger_bar.close()
