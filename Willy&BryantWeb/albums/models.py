from django.db import models
from django.contrib.auth.models import User
import os
from datetime import date


def cover_upload_path(instance, filename):
    # Generar un nombre único para el archivo
    ext = filename.split('.')[-1]
    filename = f"{instance.band}_{instance.title}_{instance.id}.{ext}".replace(
        ' ', '_').lower()
    return os.path.join('covers', filename)


class Album(models.Model):
    title = models.CharField(max_length=200)
    band = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, default='Metal')
    release_date = models.DateField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    cover = models.ImageField(
        upload_to=cover_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.band}"

    class Meta:
        ordering = ['-created_at']
