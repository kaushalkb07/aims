from django.contrib import admin
from .models import Product, RFIDEntry, StockMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_rfid_tag', 'category', 'quantity', 'location', 'timestamp', 'last_updated')
    list_filter = ('category', 'location')  # ✅ Fixed location error
    ordering = ('-timestamp',)

    def get_rfid_tag(self, obj):
        return obj.assigned_rfid.rfid_tag if obj.assigned_rfid else "No RFID"
    get_rfid_tag.short_description = "RFID Tag"

@admin.register(RFIDEntry)
class RFIDEntryAdmin(admin.ModelAdmin):
    list_display = ('rfid_tag', 'rfid_tag_description', 'status', 'timestamp')
    ordering = ('-timestamp',)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'rfid_tag', 'quantity', 'action', 'timestamp_in', 'timestamp_out')
    list_filter = ('action',)
    ordering = ('-timestamp_in',)
