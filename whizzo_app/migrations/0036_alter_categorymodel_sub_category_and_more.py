# Generated by Django 4.2.11 on 2024-05-27 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0035_testimonialmodel_country_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='sub_category',
            field=models.IntegerField(choices=[(1, 'QUESTIONS WITH OPTIONS'), (2, 'FLASH CARDS'), (3, 'ABILITIES'), (4, 'ACHIEVEMENTS'), (5, 'UPLOAD FILES OR BOOKS'), (6, 'UPLOAD PDF OR IMAGE')], default=0),
        ),
        migrations.CreateModel(
            name='FileSumarizationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sub_category', models.IntegerField(choices=[(1, 'QUESTIONS WITH OPTIONS'), (2, 'FLASH CARDS'), (3, 'ABILITIES'), (4, 'ACHIEVEMENTS'), (5, 'UPLOAD FILES OR BOOKS'), (6, 'UPLOAD PDF OR IMAGE')], default=0)),
                ('result', models.JSONField(default=list)),
                ('media', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='whizzo_app.uploadmediamodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'FileSumarization',
            },
        ),
    ]
