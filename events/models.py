from django.db import models

# Create your models here.
from application.models import Application


class Events(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
