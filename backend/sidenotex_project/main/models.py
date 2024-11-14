from django.db import models
import uuid
from django.utils import timezone
from django.core.validators import URLValidator


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
    
class Sidenote(models.Model):
    url = models.URLField(max_length=2000, validators=[URLValidator()])
    text = models.TextField()
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    domain = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.domain and self.author:
            self.domain = self.author.user_domain
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author.email} - {self.url[:50]}..."

    class Meta:
        indexes = [
            models.Index(fields=['domain']),
            models.Index(fields=['author']),
        ]