from django.db import models
from django.core.validators import RegexValidator
import ipaddress

# Create your models here.
class Zakaznici(models.Model):
    tel_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Zadejte telefon ve formatu +420123456789 nebo 123456789.")
    #
    jmeno = models.CharField(max_length=50)
    prijmeni = models.CharField(max_length=50)
    telefon = models.CharField(validators=[tel_regex], max_length=16, blank=True)
    email = models.EmailField(max_length=50)
    def __str__(self):
        return "%s %s" % (self.jmeno, self.prijmeni)
    def ma_email(self):
        return self.email!=None


class Ipv4(models.Model):
    ip_adresa = models.GenericIPAddressField(protocol='IPv4', unpack_ipv4=False)
    aktivni = models.BooleanField(default=False)
    id_zakaznika = models.ForeignKey(Zakaznici, on_delete=models.CASCADE)
    #TODO jen zkusebni
    votes = models.IntegerField(default=0)
    def __str__(self):
        return "%s" % (ipaddress.ip_address(self.ip_adresa))
