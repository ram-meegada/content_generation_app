# Generated by Django 4.2.11 on 2024-05-27 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0040_reseaerchmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reseaerchmodel',
            name='specify_reference',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reseaerchmodel',
            name='tone_of_voice',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
