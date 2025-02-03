from django.contrib import admin
from .models import RFIDEntry, Product, StockMovement

# Register RFIDEntry model in admin
class RFIDEntryAdmin(admin.ModelAdmin):
    list_display = ('rfid_tag', 'rfid_tag_description', 'timestamp', 'status')
    search_fields = ('rfid_tag', 'rfid_tag_description')
    list_filter = ('status',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

# Register Product model in admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'rfid_tag', 'category', 'quantity', 'location', 'last_updated')
    search_fields = ('name', 'rfid_tag', 'category')
    list_filter = ('category', 'location')
    ordering = ('-last_updated',)
    list_per_page = 20

# Register StockMovement model in admin
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'rfid_tag', 'quantity', 'action', 'timestamp')
    search_fields = ('product_name', 'rfid_tag')
    list_filter = ('action',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

# Registering models in admin
admin.site.register(RFIDEntry, RFIDEntryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(StockMovement, StockMovementAdmin)
