# Generated by Django 3.0.3 on 2020-12-02 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isp', '0008_vytvoreno_adresy_tarify_tarifni_skupiny'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipv4',
            name='votes',
        ),
    ]