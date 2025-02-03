import os
import pandas as pd
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Product, StockMovement

# Path to RFID exported Excel file
EXCEL_FILE_PATH = "/path/to/your/rfid_stock_data.xlsx"

def update_stock_from_excel():
    if not os.path.exists(EXCEL_FILE_PATH):
        print("Excel file not found!")
        return
    
    df = pd.read_excel(EXCEL_FILE_PATH, engine='openpyxl')

    for _, row in df.iterrows():
        timestamp = make_aware(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
        action = row["action"].upper()

        product, created = Product.objects.get_or_create(
            rfid_tag=row["rfid_tag"],
            defaults={"name": row["name"], "category": row["category"], "quantity": 0, "location": row["location"]}
        )

        if action == "IN":
            product.quantity += row["quantity"]
        elif action == "OUT" and product.quantity >= row["quantity"]:
            product.quantity -= row["quantity"]
        else:
            print(f"Insufficient stock for {row['rfid_tag']}!")

        product.save()

        # Log stock movement
        StockMovement.objects.create(
            rfid_tag=product,
            action=action,
            quantity=row["quantity"],
            timestamp=timestamp
        )

    print("Stock database updated successfully from RFID Excel.")
