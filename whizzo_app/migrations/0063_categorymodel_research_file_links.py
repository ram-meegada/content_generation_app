# Generated by Django 4.2.11 on 2024-06-21 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0062_categorymodel_page_categorymodel_reference_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='research_file_links',
            field=models.JSONField(default=list),
        ),
    ]
