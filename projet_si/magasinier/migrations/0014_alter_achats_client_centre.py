# Generated by Django 5.0 on 2023-12-26 03:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0013_remove_achats_client_magasinier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achats_client',
            name='Centre',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='magasinier.centre'),
        ),
    ]
