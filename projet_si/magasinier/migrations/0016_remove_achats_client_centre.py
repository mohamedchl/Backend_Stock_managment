# Generated by Django 5.0 on 2023-12-26 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0015_alter_client_nomcl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achats_client',
            name='Centre',
        ),
    ]
