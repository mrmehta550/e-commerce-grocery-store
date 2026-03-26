from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider')
    business_name = models.CharField(max_length=255, blank=True)
    service_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name