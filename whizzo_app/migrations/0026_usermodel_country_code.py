# Generated by Django 4.2.11 on 2024-05-07 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0025_faqmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='country_code',
            field=models.CharField(default='', max_length=17),
        ),
    ]
