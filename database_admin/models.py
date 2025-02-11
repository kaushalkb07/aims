from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class RFIDEntry(models.Model):
    CATEGORY_CHOICES = (
        ('NONE', 'None'),
        ('ASSIGNED', 'Assigned'),
        ('NOT ASSIGNED', 'Not Assigned'),
    )
    id = models.AutoField(primary_key=True)
    rfid_tag = models.CharField(max_length=100, unique=True)
    rfid_tag_description = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='NOT ASSIGNED')
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.rfid_tag} ({self.status})"

class Product(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    assigned_rfid = models.ForeignKey(RFIDEntry, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ Track who added the product
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} ({self.assigned_rfid.rfid_tag if self.assigned_rfid else 'No RFID'})"


class StockMovement(models.Model):
    sno = models.AutoField(primary_key=True)
    rfid_tag = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    ACTION_CHOICES = [('IN', 'In'), ('OUT', 'Out')]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp_in = models.DateTimeField(auto_now_add=True)
    timestamp_out = models.DateTimeField(auto_now=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ Track user

    def __str__(self):
        return f"{self.product_name} ({self.rfid_tag}) - {self.action}"
