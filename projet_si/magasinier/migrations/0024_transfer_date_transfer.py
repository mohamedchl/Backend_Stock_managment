# Generated by Django 5.0 on 2023-12-26 23:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0023_rename_date_paye_credit_date_modification'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='Date_transfer',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
