from django.urls import path
from .views import trigger_manual_stock_update
from . import views

urlpatterns = [
    path('update-stock/', trigger_manual_stock_update, name='update-stock'),
    path('upload/rfid/', views.upload_rfid_entry, name='upload_rfid_entry'),
    path('upload/product/', views.upload_product, name='upload_product'),
    path('upload/stock/', views.upload_stock_movement, name='upload_stock_movement'),
]
