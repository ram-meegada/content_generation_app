# Generated by Django 4.2.11 on 2024-07-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0084_notetakingmodel_note_screenshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='notetakingmodel',
            name='canvas_height',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
