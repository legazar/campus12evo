# Generated by Django 5.0.6 on 2024-07-29 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_remove_utilisateur_epreuve'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Utilisateur',
        ),
    ]