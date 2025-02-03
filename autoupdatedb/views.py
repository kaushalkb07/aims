from django.http import JsonResponse
from .utils import update_stock_from_excel

def trigger_manual_stock_update(request):
    update_stock_from_excel()  # Run update immediately
    return JsonResponse({"message": "Stock update triggered"})
