# Generated by Django 4.2.11 on 2024-05-06 05:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0011_achievementmodel_subject_alter_abilitymodel_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abilitymodel',
            name='answer_option',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=255), default=[], size=None),
        ),
    ]
