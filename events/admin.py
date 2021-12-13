from django.contrib import admin

# Register your models here.
from events.models import Events

admin.site.register(Events)
