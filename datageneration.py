import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data for RFIDEntry
rfid_entries = [
    {
        'id': i+1, 
        'rfid_tag': f'RFID-{100+i}', 
        'rfid_tag_description': f'RFID Tag {100+i} Description',
        'timestamp': datetime.now() - timedelta(days=random.randint(0,30)),
        'status': random.choice(['ACTIVE', 'INACTIVE'])
    } for i in range(25)
]
rfid_df = pd.DataFrame(rfid_entries)
rfid_df.to_excel('rfid_entries.xlsx', index=False)

# Sample data for Product
products = [
    {
        'rfid_tag': f'PROD-{200+i}',
        'name': random.choice(['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera', 
                                'Smartwatch', 'Monitor', 'Keyboard', 'Mouse', 'Speaker']),
        'category': random.choice(['Electronics', 'Computer', 'Mobile', 'Accessories', 'Wearables']),
        'quantity': random.randint(1, 100),
        'location': random.choice(['Warehouse A', 'Warehouse B', 'Store 1', 'Store 2', None]),
        'last_updated': datetime.now() - timedelta(days=random.randint(0,30))
    } for i in range(25)
]
product_df = pd.DataFrame(products)
product_df.to_excel('products.xlsx', index=False)

# Sample data for StockMovement
stock_movements = [
    {
        'rfid_tag': f'MOV-{300+i}',
        'product_name': random.choice(['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera', 
                                        'Smartwatch', 'Monitor', 'Keyboard', 'Mouse', 'Speaker']),
        'quantity': random.randint(1, 50),
        'action': random.choice(['IN', 'OUT']),
        'timestamp': datetime.now() - timedelta(days=random.randint(0,30))
    } for i in range(25)
]
stock_movement_df = pd.DataFrame(stock_movements)
stock_movement_df.to_excel('stock_movements.xlsx', index=False)

print("Excel files generated successfully!")