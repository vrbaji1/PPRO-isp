# Generated by Django 3.0.3 on 2020-09-21 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isp', '0004_telefon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zakaznici',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]
