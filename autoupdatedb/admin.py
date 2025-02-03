from django.contrib import admin
from .models import Product, StockMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'rfid_tag', 'quantity', 'category', 'location', 'last_updated')
    search_fields = ('name', 'rfid_tag')

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('rfid_tag', 'action', 'quantity', 'timestamp')
    search_fields = ('rfid_tag__rfid_tag',)
