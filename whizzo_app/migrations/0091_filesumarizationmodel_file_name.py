# Generated by Django 4.2.11 on 2024-08-30 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0090_categorymodel_binary_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesumarizationmodel',
            name='file_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
