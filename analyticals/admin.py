from django.contrib import admin

# Register your models here.
from .models import Stock, PortEntries

admin.site.register(Stock)
admin.site.register(PortEntries)
