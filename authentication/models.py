from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    base32_secret = models.CharField(max_length=16, unique=True)  # Unique secret for OTP generation
    otp = models.CharField(max_length=6, null=True, blank=True)  # Temporary OTP storage
    otp_generated_time = models.DateTimeField(null=True, blank=True)  # OTP timestamp