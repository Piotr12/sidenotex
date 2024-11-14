from django.db import models
import uuid
from django.utils import timezone

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.CharField(max_length=19)  # 'YYYY-MM-DD HH:MM:SS'
    created_ip = models.GenericIPAddressField()
    user_domain = models.CharField(max_length=255)  # New field

    def save(self, *args, **kwargs):
        if self.email:
            self.user_domain = self.email.split('@')[1]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email