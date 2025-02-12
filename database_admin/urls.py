from django.urls import path
from . import views

urlpatterns = [
    path('upload_rfid/', views.upload_rfid_entry, name='upload_rfid_entry'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('upload_stock/', views.upload_stock_movement, name='upload_stock_movement'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('delete_product/<int:product_sno>/', views.delete_product, name='delete_product'),
    path('edit_product/<int:product_sno>/', views.edit_product, name='edit_product'),
    path('rfid_list/', views.rfid_list, name='rfid_list'),
    path('add_rfid/', views.add_rfid, name='add_rfid'),
    path('edit_rfid/<int:rfid_id>/', views.edit_rfid, name='edit_rfid'),
    path('delete_rfid/<int:rfid_id>/', views.delete_rfid, name='delete_rfid'),
    path("fetch-firebase/", views.fetch_firebase_data, name="fetch_firebase_data"),
    path("stock-movement/", views.stock_movement_list, name="stock_movement_list"),

]
