from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from database_admin.models import RFIDEntry, Product, StockMovement

@login_required
def dashboard(request):
    # Analyze RFID entries
    active_rfid_count = RFIDEntry.objects.filter(status='ACTIVE').count()
    inactive_rfid_count = RFIDEntry.objects.filter(status='INACTIVE').count()
    
    # Analyze Product data
    total_products = Product.objects.count()
    total_quantity = Product.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    
    # Analyze StockMovement data
    total_in = StockMovement.objects.filter(action='IN').aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_out = StockMovement.objects.filter(action='OUT').aggregate(Sum('quantity'))['quantity__sum'] or 0
    
    # Prepare data for Chart.js
    chart_data = {
        'active_rfid_count': active_rfid_count,
        'inactive_rfid_count': inactive_rfid_count,
        'total_products': total_products,
        'total_quantity': total_quantity,
        'total_in': total_in,
        'total_out': total_out,
    }
    
    context = {
        'chart_data': chart_data,
    }
    
    return render(request, 'dashboard/dashboard.html', context)  # Ensure the template exists