# Generated by Django 4.2.5 on 2023-11-17 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_enspd_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo_Ecole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre_ecole', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.DeleteModel(
            name='Enspd',
        ),
    ]