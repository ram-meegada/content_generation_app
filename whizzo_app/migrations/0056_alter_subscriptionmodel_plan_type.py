# Generated by Django 4.2.11 on 2024-06-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0055_fileconversationmodel_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionmodel',
            name='plan_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Free Trial'), (2, 'Monthly'), (3, 'Quaterly'), (4, 'Yearly')], null=True),
        ),
    ]
