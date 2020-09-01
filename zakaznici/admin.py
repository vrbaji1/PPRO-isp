from django.contrib import admin

# Register your models here.
from .models import Zakaznici, Ipv4

admin.site.register(Zakaznici)
admin.site.register(Ipv4)
