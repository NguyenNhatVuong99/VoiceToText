from django.db import models

# Create your models here.

class AudioFile(models.Model):
    audio = models.FileField(upload_to='audio/')
    transcript = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio file from {self.created_at}"
