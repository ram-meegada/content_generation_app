# Generated by Django 4.2.11 on 2024-07-24 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0083_notetakingmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='notetakingmodel',
            name='note_screenshot',
            field=models.TextField(default=''),
        ),
    ]
