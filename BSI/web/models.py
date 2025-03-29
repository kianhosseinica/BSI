# web/models.py
from django.db import models
import json
from django.contrib.auth.models import User
import random


class CostEstimate(models.Model):
    # Link the cost estimate to a user (optional if not all estimates have a user)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cost_estimates', null=True, blank=True)

    method = models.CharField(max_length=50)
    website_type = models.CharField(max_length=100)
    # We'll store arrays (technologies and features) and the additional details as JSON strings.
    technologies = models.TextField(help_text="JSON-encoded list of technologies")
    features = models.TextField(help_text="JSON-encoded list of features")
    traffic = models.CharField(max_length=100, blank=True)
    idea = models.TextField(blank=True)
    timeline = models.CharField(max_length=50, blank=True)
    maintenance = models.BooleanField(default=False)
    additional_details = models.TextField(help_text="JSON-encoded additional details", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.website_type} estimate by method {self.method}"


from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, unique=True)
    # Optional duplicate fields – these already exist in User,
    # but you might want them here for easier access or additional flags.
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    # For example, a flag indicating whether the email has been verified.
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile for {self.user.username}"




import random

def generate_otp(num_digits=4):
    """Generate a random OTP with the given number of digits."""
    range_start = 10**(num_digits-1)
    range_end = (10**num_digits) - 1
    return str(random.randint(range_start, range_end))
