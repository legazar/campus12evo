# Generated by Django 5.0.6 on 2024-07-04 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_utilisateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='correction',
            name='image_apercu',
            field=models.ImageField(null=True, upload_to='apercu_image_correction'),
        ),
    ]