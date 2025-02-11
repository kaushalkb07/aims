import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RFIDEntry, Product, StockMovement
from .forms import ProductForm

# ✅ Helper function to handle CSV/Excel upload
def handle_uploaded_file(file, model_class, user=None):
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
            data = row.to_dict()
            
            # ✅ If model has a 'user' field, assign the logged-in user
            if hasattr(model_class, 'user') and user:
                data['user'] = user

            # ✅ Ensure ForeignKey relations are assigned correctly
            if 'assigned_rfid' in data and isinstance(data['assigned_rfid'], str):
                data['assigned_rfid'] = RFIDEntry.objects.filter(rfid_tag=data['assigned_rfid']).first()

            model_class.objects.create(**data)

        return True
    except Exception as e:
        return f"Error: {e}"

# ✅ View for uploading RFIDEntry data
@login_required
def upload_rfid_entry(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = handle_uploaded_file(file, RFIDEntry, request.user)  # ✅ Pass user

        if result is True:
            messages.success(request, 'RFID entries uploaded successfully.')
        else:
            messages.error(request, result)

    return render(request, 'dataupload/upload.html', {'model': 'RFIDEntry'})

# ✅ View for uploading Product data
@login_required
def upload_product(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = handle_uploaded_file(file, Product, request.user)  # ✅ Pass user

        if result is True:
            messages.success(request, 'Products uploaded successfully.')
        else:
            messages.error(request, result)

    return render(request, 'dataupload/upload.html', {'model': 'Product'})

# ✅ View for uploading StockMovement data
@login_required
def upload_stock_movement(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = handle_uploaded_file(file, StockMovement, request.user)  # ✅ Pass user

        if result is True:
            messages.success(request, 'Stock movements uploaded successfully.')
        else:
            messages.error(request, result)

    return render(request, 'dataupload/upload.html', {'model': 'StockMovement'})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list
    else:
        form = ProductForm()  

    return render(request, 'dashboard/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, "dashboard/product_list.html", {"products": products})