from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class RFIDEntry(models.Model):
    rfid_tag = models.CharField(max_length=100, unique=True)
    rfid_tag_description = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[("Not Assigned", "Not Assigned"), ("Assigned", "Assigned")], default="Not Assigned")
    timestamp = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.rfid_tag} ({self.status})"

class Product(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    assigned_rfid = models.OneToOneField(RFIDEntry, on_delete=models.CASCADE, null=True, blank=True, related_name="product")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if self.pk:
            old_product = Product.objects.filter(pk=self.pk).first()
            if old_product and old_product.assigned_rfid and old_product.assigned_rfid != self.assigned_rfid:
                old_product.assigned_rfid.status = 'Not Assigned'
                old_product.assigned_rfid.save()

        if self.assigned_rfid:
            self.assigned_rfid.status = 'Assigned'
            self.assigned_rfid.save()

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.assigned_rfid.rfid_tag if self.assigned_rfid else 'No RFID'})"

class StockMovement(models.Model):
    sno = models.AutoField(primary_key=True)
    rfid_tag = models.ForeignKey(RFIDEntry, on_delete=models.CASCADE, to_field="rfid_tag")
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    ACTION_CHOICES = [('IN', 'In'), ('OUT', 'Out')]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp_in = models.DateTimeField(default=now, null=True, blank=True)
    timestamp_out = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} ({self.rfid_tag.rfid_tag}) - {self.action}"
