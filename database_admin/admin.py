from django.contrib import admin
from .models import RFIDEntry, Product, StockMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'assigned_rfid', 'user', 'timestamp')  # ✅ Show user
    list_filter = ('category', 'user')  # ✅ Allow filtering by user
    search_fields = ('name', 'assigned_rfid__rfid_tag', 'user__username')  # ✅ Allow searching by RFID & user
    autocomplete_fields = ['assigned_rfid']  # ✅ Ensure autocomplete works correctly

from django.contrib import admin
from .models import RFIDEntry

@admin.register(RFIDEntry)
class RFIDEntryAdmin(admin.ModelAdmin):
    list_display = ('rfid_tag', 'rfid_tag_description', 'status', 'user', 'timestamp')  # ✅ Columns shown in admin
    list_filter = ('status', 'timestamp')  # ✅ Filters for quick access
    search_fields = ('rfid_tag', 'rfid_tag_description')  # ✅ Searchable fields
    ordering = ('-timestamp',)  # ✅ Latest entries appear first
    readonly_fields = ('timestamp',)  # ✅ Prevent manual timestamp edits


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'rfid_tag', 'quantity', 'action', 'timestamp_in', 'timestamp_out', 'user')
    list_filter = ('action', 'user')  # ✅ Filter by user
    search_fields = ['product_name', 'rfid_tag', 'user__username']  # ✅ Search by username
