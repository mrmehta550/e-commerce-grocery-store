from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Provider

User = get_user_model()

# Removed the signal as Provider creation is now handled in RegisterForm