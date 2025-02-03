from django.urls import path
from .views import trigger_manual_stock_update, upload_file
from . import views

urlpatterns = [
    path('update-stock/', trigger_manual_stock_update, name='update-stock'),
    path('upload/', views.upload_file, name='upload_file'),
]
