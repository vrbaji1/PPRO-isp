from django.contrib import admin

# Register your models here.
from .models import Zakaznici, Ipv4



class Ipv4Inline(admin.TabularInline):
    model = Ipv4
    #kolik se vzdy zobrazi volnych navic
    extra = 1


class ZakazniciAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Jméno',           {'fields': ['jmeno','prijmeni']}),
        ('Kontaktní údaje', {'fields': ['telefon','email']}),
    ]
    inlines = [Ipv4Inline]
    list_display = ('prijmeni', 'jmeno', 'telefon', 'email')
    list_filter = ['prijmeni']
    search_fields = ['prijmeni', 'jmeno', 'telefon', 'email']

admin.site.register(Zakaznici, ZakazniciAdmin)
#admin.site.register(Ipv4)
