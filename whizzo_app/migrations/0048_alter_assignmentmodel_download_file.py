# Generated by Django 4.2.11 on 2024-06-06 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0047_assignmentmodel_download_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentmodel',
            name='download_file',
            field=models.TextField(default=''),
        ),
    ]
