from django.urls import path
from . import views

urlpatterns = [
    path('upload/rfid/', views.upload_rfid_entry, name='upload_rfid_entry'),
    path('upload/product/', views.upload_product, name='upload_product'),
    path('upload/stock/', views.upload_stock_movement, name='upload_stock_movement'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_list/', views.product_list, name='product_list'),
    
]
