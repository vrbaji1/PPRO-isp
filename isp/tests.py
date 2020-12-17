from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

# Create your tests here.
# uvod psani textu zde: https://docs.djangoproject.com/en/3.0/intro/tutorial05/

from .models import Zakaznici


class LoginTests(TestCase):

    def _vytvor_uzivatele(self):
        """
        Vytvori uzivatele pro testovani.
        """
        self.client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create_user('testovani', 'testovani@test.cz', 'testovaci_heslo')

    def test_pristup_pred_prihlasenim(self):
        """
        Bez prihlaseni nemam pristup k obsahu.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_pristup_spatne_heslo(self):
        """
        Pristup se spatnym heslem.
        """
        self._vytvor_uzivatele()
        self.client.login(username='testovani', password='spatne_heslo')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_pristup_dobre_heslo(self):
        """
        Pristup se spatnym heslem.
        """
        self._vytvor_uzivatele()
        self.client.login(username='testovani', password='testovaci_heslo')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ZakazniciModelTests(TestCase):

    def test_ma_email_bez_mailu(self):
        """
        U zakaznika, ktery nema email, by melo vracet False.
        Testuje jak prazdny retezec, tak None.
        """
        zakaznik = Zakaznici(email=None)
        self.assertIs(zakaznik.ma_email(), False)
        zakaznik = Zakaznici(email="")
        self.assertIs(zakaznik.ma_email(), False)

    def test_ma_email_s_mailem(self):
        """
        U zakaznika, ktery ma email, by melo vracet True.
        Testuje jak prazdny retezec, tak None.
        """
        zakaznik = Zakaznici(email="neco@neco.cz")
        self.assertIs(zakaznik.ma_email(), True)
