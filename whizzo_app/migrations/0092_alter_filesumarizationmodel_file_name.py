# Generated by Django 4.2.11 on 2024-08-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0091_filesumarizationmodel_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filesumarizationmodel',
            name='file_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
