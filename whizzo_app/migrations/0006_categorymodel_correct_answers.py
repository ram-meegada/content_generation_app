# Generated by Django 4.2.11 on 2024-04-25 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0005_alter_categorymodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='correct_answers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
