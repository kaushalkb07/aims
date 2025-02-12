import pandas as pd
import firebase_admin
from firebase_admin import db
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RFIDEntry, Product, StockMovement
from .forms import ProductForm, RFIDEntryForm
from django.urls import reverse
from datetime import datetime
from django.utils.timezone import make_aware

# Helper function to handle CSV/Excel upload
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
            
            #  If model has a 'user' field, assign the logged-in user
            if hasattr(model_class, 'user') and user:
                data['user'] = user

            #  Ensure ForeignKey relations are assigned correctly
            if 'assigned_rfid' in data and isinstance(data['assigned_rfid'], str):
                data['assigned_rfid'] = RFIDEntry.objects.filter(rfid_tag=data['assigned_rfid']).first()

            model_class.objects.create(**data)

        return True
    except Exception as e:
        return f"Error: {e}"

# View for uploading RFIDEntry data
@login_required
def upload_rfid_entry(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = handle_uploaded_file(file, RFIDEntry, request.user)  #  Pass user

        if result is True:
            messages.success(request, 'RFID entries uploaded successfully.')
        else:
            messages.error(request, result)

    return render(request, 'dataupload/upload.html', {'model': 'RFIDEntry'})

#  View for uploading Product data
@login_required
def upload_product(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = handle_uploaded_file(file, Product, request.user)  #  Pass user

        if result is True:
            messages.success(request, 'Products uploaded successfully.')
        else:
            messages.error(request, result)

    return render(request, 'dataupload/upload.html', {'model': 'Product'})

#  View for uploading StockMovement data
@login_required
def upload_stock_movement(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = handle_uploaded_file(file, StockMovement, request.user)  #  Pass user

        if result is True:
            messages.success(request, 'Stock movements uploaded successfully.')
        else:
            messages.error(request, result)

    return render(request, 'dataupload/upload.html', {'model': 'StockMovement'})

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  #  Assign the logged-in user
            if product.assigned_rfid:
                product.assigned_rfid.status = 'Assigned'
                product.assigned_rfid.save()
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('product_list')  #  Redirect to the product list page
    else:
        form = ProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form})

def product_list(request):
    query = request.GET.get('query', '')

    if query:
        products = Product.objects.filter(name__icontains=query)  # Search by Product Name
    else:
        products = Product.objects.all()

    return render(request, "dashboard/product_list.html", {"products": products, "query": query})


def delete_product(request, product_sno):
    product = get_object_or_404(Product, sno=product_sno)
    
    #  If product has an assigned RFID, update its status
    if product.assigned_rfid:
        product.assigned_rfid.status = "Not Assigned"
        product.assigned_rfid.save()

    product.delete()  #  Now delete the product
    
    messages.success(request, "Product deleted successfully and RFID status updated.")
    return redirect('product_list')  #  Redirect to product list after deletion

def edit_product(request, product_sno):  
    product = get_object_or_404(Product, sno=product_sno)  

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product_list')  
    else:
        form = ProductForm(instance=product)  # ✅ This pre-fills the form fields

    return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})

@login_required
def add_rfid(request):
    if request.method == "POST":
        form = RFIDEntryForm(request.POST)
        if form.is_valid():
            rfid_entry = form.save(commit=False)
            rfid_entry.user = request.user  # Track the user who added the entry
            rfid_entry.save()
            messages.success(request, "RFID Entry added successfully!")
            return redirect('rfid_entries_list')
    else:
        form = RFIDEntryForm()
    return render(request, 'dashboard/add_rfid_entries.html', {'form': form})

@login_required
def edit_rfid(request, entry_id):
    rfid_entry = get_object_or_404(RFIDEntry, id=entry_id)

    if request.method == "POST":
        form = RFIDEntryForm(request.POST, instance=rfid_entry)
        if form.is_valid():
            form.save()
            messages.success(request, "RFID Entry updated successfully!")
            return redirect('rfid_entries_list')
    else:
        form = RFIDEntryForm(instance=rfid_entry)

    return render(request, 'dashboard/edit_rfid_entries.html', {'form': form, 'rfid_entry': rfid_entry})

@login_required
def delete_rfid(request, entry_id):
    rfid_entry = get_object_or_404(RFIDEntry, id=entry_id)
    rfid_entry.delete()
    messages.success(request, "RFID Entry deleted successfully!")
    return redirect('rfid_entries_list')

@login_required
def rfid_list(request):
    query = request.GET.get('query', '')

    if query:
        rfid_entries = RFIDEntry.objects.filter(rfid_tag__icontains=query)  # Search by RFID tag
    else:
        rfid_entries = RFIDEntry.objects.all()

    return render(request, "dashboard/rfid_entries_list.html", {"rfid_entries": rfid_entries, "query": query})

# View to list stock movements
@login_required
def stock_movement_list(request):
    stock_movements = StockMovement.objects.all().order_by('-timestamp_in')
    return render(request, "dashboard/stock_movement_list.html", {"stock_movements": stock_movements})

# View to fetch data from Firebase and store in the database
@login_required
def fetch_firebase_data(request):
    try:
        ref = db.reference("/")  # Firebase Root
        data = ref.get()

        if not data:
            return render(request, "dashboard/fetch_firebase.html", {"message": "No data found in Firebase."})

        product_entries = data.get("product_entries", {})
        product_exits = data.get("product_exits", {})

        # ✅ Process product entries (Stock IN)
        for tag_id, details in product_entries.items():
            process_stock_movement(details, action="IN")

        # ✅ Process product exits (Stock OUT)
        for tag_id, details in product_exits.items():
            process_stock_movement(details, action="OUT")

        return render(request, "dashboard/fetch_firebase.html", {"message": "Firebase data fetched and stored successfully!"})

    except Exception as e:
        return render(request, "dashboard/fetch_firebase.html", {"message": f"Error fetching data: {str(e)}"})

def process_stock_movement(details, action):
    rfid_tag_value = details.get("tagID")  # ✅ Ensure correct key from Firebase

    # ✅ Convert integer timestamp to datetime
    timestamp = make_aware(datetime.utcfromtimestamp(details.get("timestamp", 0)))

    # ✅ Fetch RFID Entry using rfid_tag
    rfid_entry = RFIDEntry.objects.filter(rfid_tag=rfid_tag_value).first()
    if not rfid_entry:
        print(f"RFID {rfid_tag_value} not found in the database.")
        return

    # ✅ Fetch Product using RFID
    product = Product.objects.filter(assigned_rfid=rfid_entry.rfid_tag).first()
    product_name = product.name if product else "Unknown"
    quantity = product.quantity if product else 0

    # ✅ Store Stock Movement (Using Only rfid_tag, No ID)
    stock_movement, created = StockMovement.objects.get_or_create(
        rfid_tag=rfid_tag_value,  # ✅ Use rfid_tag as unique identifier
        action=action,
        defaults={
            "product_name": product_name,
            "quantity": quantity,
            "timestamp_in": timestamp if action == "IN" else None,
            "timestamp_out": timestamp if action == "OUT" else None,
        }
    )

    if not created:
        if action == "IN":
            stock_movement.timestamp_in = timestamp
        elif action == "OUT":
            stock_movement.timestamp_out = timestamp
        stock_movement.product_name = product_name
        stock_movement.quantity = quantity
        stock_movement.save()

    print(f"Stock movement recorded for {rfid_tag_value} - {action}")










