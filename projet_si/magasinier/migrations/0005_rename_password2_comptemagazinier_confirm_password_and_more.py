# Generated by Django 5.0 on 2024-01-19 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0004_rename_password_comptemagazinier_password1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comptemagazinier',
            old_name='password2',
            new_name='confirm_password',
        ),
        migrations.RenameField(
            model_name='comptemagazinier',
            old_name='password1',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='compteresponsable',
            old_name='password2',
            new_name='confirm_password',
        ),
        migrations.RenameField(
            model_name='compteresponsable',
            old_name='password1',
            new_name='password',
        ),
    ]
