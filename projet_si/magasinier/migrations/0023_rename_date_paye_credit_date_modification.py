# Generated by Django 5.0 on 2023-12-26 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0022_remove_paye_credit_somme_paye'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paye_credit',
            old_name='date',
            new_name='date_modification',
        ),
    ]
