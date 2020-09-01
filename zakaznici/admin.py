from django.contrib import admin

# Register your models here.
from .models import Zakaznici, Ipv4

class ZakazniciAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Jméno',           {'fields': ['jmeno','prijmeni']}),
        ('Kontaktní údaje', {'fields': ['telefon','email']}),
    ]

admin.site.register(Zakaznici, ZakazniciAdmin)
admin.site.register(Ipv4)
