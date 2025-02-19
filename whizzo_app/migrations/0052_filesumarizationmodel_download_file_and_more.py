# Generated by Django 4.2.11 on 2024-06-11 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0051_notificationmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesumarizationmodel',
            name='download_file',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='profile_status',
            field=models.IntegerField(choices=[(1, 'SIGNUP_COMPLETED'), (2, 'OTP_VERIFIED'), (3, 'PROFILE_UPDATED')], default=0),
        ),
    ]
