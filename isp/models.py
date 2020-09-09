from django.db import models
import ipaddress

# Create your models here.
class Zakaznici(models.Model):
    jmeno = models.CharField(max_length=50)
    prijmeni = models.CharField(max_length=50)
    telefon = models.IntegerField()
    email = models.CharField(max_length=50)
    def __str__(self):
        return "%s %s" % (self.jmeno, self.prijmeni)
    def ma_email(self):
        return self.email!=None


class Ipv4(models.Model):
    ip_adresa = models.IntegerField()
    aktivni = models.CharField(max_length=1)
    id_zakaznika = models.ForeignKey(Zakaznici, on_delete=models.CASCADE)
    #TODO jen zkusebni
    votes = models.IntegerField(default=0)
    def __str__(self):
        return "%s" % (ipaddress.ip_address(self.ip_adresa))
