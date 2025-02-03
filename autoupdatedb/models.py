from django.db import models
from django.utils.timezone import now
from django.db.models import Index

class RFIDEntry(models.Model):
    CATEGORY_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'INACTIVE'),
    )
    id = models.AutoField(primary_key=True)
    rfid_tag = models.CharField(max_length=100, unique=True)
    rfid_tag_description = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')


class Product(models.Model):
    rfid_tag = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            Index(fields=['rfid_tag', 'category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.rfid_tag})"


class StockMovement(models.Model):
    rfid_tag = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    ACTION_CHOICES = [('IN', 'In'), ('OUT', 'Out')]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)  # ✅ Add this field
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} ({self.rfid_tag}) - {self.action}"

