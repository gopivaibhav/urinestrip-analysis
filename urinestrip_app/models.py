from django.db import models

class UrineStrip(models.Model):
    image = models.ImageField(upload_to='urinestrips/')
    colors_json = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
