from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Input, WasteProduct, Industry, waste_invoice])
