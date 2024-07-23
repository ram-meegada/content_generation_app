# Generated by Django 4.2.11 on 2024-07-18 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0077_alter_abilitymodel_corect_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresentationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('slides', models.IntegerField(default=6)),
                ('text', models.TextField(blank=True)),
                ('binary_data', models.JSONField(default=list)),
                ('is_arabic', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Presentation',
            },
        ),
    ]
