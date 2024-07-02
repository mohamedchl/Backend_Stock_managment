# Generated by Django 5.0 on 2023-12-25 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0007_transfer_designation'),
    ]

    operations = [
        migrations.CreateModel(
            name='reProduit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomP', models.CharField(default='Produit', max_length=50)),
                ('designation', models.CharField(max_length=100, null=True)),
                ('qte', models.IntegerField(default=1)),
                ('prix_unitaire', models.FloatField(default=0, max_length=10)),
                ('Stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasinier.stock_centre')),
            ],
        ),
    ]
