# Generated by Django 4.2.11 on 2024-06-21 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0065_categorymodel_research_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='reduces_citations',
            field=models.BooleanField(default=False),
        ),
    ]
