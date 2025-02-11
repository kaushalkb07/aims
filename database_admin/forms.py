from django import forms
from .models import RFIDEntry, Product, StockMovement

class RFIDEntryForm(forms.ModelForm):
    class Meta:
        model = RFIDEntry
        fields = ['rfid_tag', 'rfid_tag_description', 'status']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'assigned_rfid']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # ✅ Only show RFID cards that are not assigned to any product
        self.fields['assigned_rfid'].queryset = RFIDEntry.objects.filter(product=None)

        # ✅ Apply Bootstrap styling while keeping your UI
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['rfid_tag', 'product_name', 'quantity', 'action']
