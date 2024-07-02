# Generated by Django 5.0 on 2023-12-26 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0019_remove_paye_credit_payement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='somme_paye',
        ),
        migrations.AddField(
            model_name='paye_credit',
            name='somme_paye',
            field=models.FloatField(default=0, max_length=10),
        ),
    ]
