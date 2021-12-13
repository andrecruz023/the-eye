from django.db import models
import random, string


# Create your models here.

class Application(models.Model):
    session_id = models.CharField(max_length=50)
    name = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_session_id():
        session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=26))
        return session_id

