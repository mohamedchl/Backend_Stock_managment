# Generated by Django 5.0 on 2023-12-26 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0011_rename_qte_reproduit_qte_produit_primaire_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achats_client',
            name='Montant_achat',
        ),
        migrations.RemoveField(
            model_name='achats_client',
            name='solde',
        ),
    ]
