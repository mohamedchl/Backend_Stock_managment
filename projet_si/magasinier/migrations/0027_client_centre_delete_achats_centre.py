# Generated by Django 5.0 on 2023-12-27 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0026_remove_client_centre'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='Centre',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='magasinier.centre'),
        ),
        migrations.DeleteModel(
            name='Achats_centre',
        ),
    ]
