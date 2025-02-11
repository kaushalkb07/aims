from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import RFIDEntry, Product, StockMovement
from django.contrib import messages

# Helper function to handle CSV/Excel upload
def handle_uploaded_file(file, model_class):
    try:
        # Read CSV or Excel file into DataFrame
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format")

        # Iterate over the DataFrame and save each row as a model instance
        for _, row in df.iterrows():
            model_class.objects.create(**row.to_dict())
        
        return True
    except Exception as e:
        return f"Error: {e}"

# View for uploading RFIDEntry data
def upload_rfid_entry(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        result = handle_uploaded_file(file, RFIDEntry)
        
        if result is True:
            messages.success(request, 'RFID entries uploaded successfully.')
        else:
            messages.error(request, result)
    
    return render(request, 'dataupload/upload.html', {'model': 'RFIDEntry'})

# View for uploading Product data
def upload_product(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        result = handle_uploaded_file(file, Product)
        
        if result is True:
            messages.success(request, 'Products uploaded successfully.')
        else:
            messages.error(request, result)
    
    return render(request, 'dataupload/upload.html', {'model': 'Product'})

# View for uploading StockMovement data
def upload_stock_movement(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        result = handle_uploaded_file(file, StockMovement)
        
        if result is True:
            messages.success(request, 'Stock movements uploaded successfully.')
        else:
            messages.error(request, result)
    
    return render(request, 'dataupload/upload.html', {'model': 'StockMovement'})

