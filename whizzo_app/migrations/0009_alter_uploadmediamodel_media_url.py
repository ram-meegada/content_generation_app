# Generated by Django 4.2.11 on 2024-04-26 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0008_alter_uploadmediamodel_media_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmediamodel',
            name='media_url',
            field=models.CharField(default='', max_length=255),
        ),
    ]
