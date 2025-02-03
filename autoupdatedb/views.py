from django.http import JsonResponse
from .utils import update_stock_from_excel
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FileUploadForm
from .models import RFIDEntry, Product, StockMovement

def handle_uploaded_file(file):
    # Load the file using pandas
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")

    # Parse the file content and save it to the database
    for _, row in df.iterrows():
        if 'rfid_tag' in row and 'timestamp' in row:  # for RFIDEntry
            RFIDEntry.objects.create(
                rfid_tag=row['rfid_tag'],
                rfid_tag_description=row.get('rfid_tag_description', ''),
                timestamp=row['timestamp'],
                status=row.get('status', 'ACTIVE')  # Default to ACTIVE
            )
        
        if 'rfid_tag' in row and 'name' in row:  # for Product
            Product.objects.create(
                rfid_tag=row['rfid_tag'],
                name=row['name'],
                category=row['category'],
                quantity=row.get('quantity', 1),  # Default to 1 if not specified
                location=row.get('location', ''),
                last_updated=row['last_updated']
            )
        
        if 'rfid_tag' in row and 'product_name' in row:  # for StockMovement
            StockMovement.objects.create(
                rfid_tag=row['rfid_tag'],
                product_name=row['product_name'],
                quantity=row['quantity'],
                action=row['action'],
                timestamp=row['timestamp']
            )

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            handle_uploaded_file(file)
            return HttpResponse("File uploaded and data saved successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {e}")

    form = FileUploadForm()
    return render(request, 'dataupload/upload.html', {'form': form})

def trigger_manual_stock_update(request):
    update_stock_from_excel()  # Run update immediately
    return JsonResponse({"message": "Stock update triggered"})
