# Generated by Django 5.0 on 2023-12-27 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0027_client_centre_delete_achats_centre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='Centre',
        ),
    ]
