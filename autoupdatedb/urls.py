from django.urls import path
from .views import trigger_manual_stock_update

urlpatterns = [
    path('update-stock/', trigger_manual_stock_update, name='update-stock'),
]
