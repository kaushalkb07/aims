from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from database_admin.models import Product, StockMovement, RFIDEntry
from django.db.models import Sum
from database_admin.views import fetch_firebase_data  # Import from the Firebase handling app

def dashboard(request):
    # Count total products
    total_products = Product.objects.count()

    # Count total "IN" movements
    total_in_movement = StockMovement.objects.filter(action="IN").count()

    # Count total "OUT" movements
    total_out_movement = StockMovement.objects.filter(action="OUT").count()

    # Fetch recent stock movements (latest 5)
    recent_movements = StockMovement.objects.order_by("-timestamp_in")[:5]

    context = {
        "total_products": total_products,
        "total_in_movement": total_in_movement,  # Updated variable name
        "total_out_movement": total_out_movement,  # Updated variable name
        "recent_movements": recent_movements
    }
    return render(request, "dashboard/dashboard.html", context)

@login_required
def sync_firebase(request):
    fetch_firebase_data(request)  # Call function to sync data
    messages.success(request, "Firebase data synced successfully!")
    return redirect("dashboard")

@login_required
def product_list(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, "dashboard/product_list.html", {"products": products, "query": query})

@login_required
def stock_movement_list(request):
    query = request.GET.get("query", "").strip()
    stock_movements = StockMovement.objects.filter(product_name__icontains=query) if query else StockMovement.objects.all()
    return render(request, "dashboard/stock_movement_list.html", {"stock_movements": stock_movements, "query": query})
