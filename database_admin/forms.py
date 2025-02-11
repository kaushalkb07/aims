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

        if self.instance and self.instance.assigned_rfid:
            # Show unassigned RFIDs + the already assigned one
            self.fields['assigned_rfid'].queryset = (
                RFIDEntry.objects.filter(status='Not Assigned') | 
                RFIDEntry.objects.filter(id=self.instance.assigned_rfid.id)
            )
        else:
            # Only show RFIDs that are not assigned
            self.fields['assigned_rfid'].queryset = RFIDEntry.objects.filter(status='Not Assigned')

        # Apply Bootstrap styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['rfid_tag', 'product_name', 'quantity', 'action']
