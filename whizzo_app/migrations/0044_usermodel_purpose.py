# Generated by Django 4.2.11 on 2024-05-30 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0043_abilitymodel_corect_answer_abilitymodel_is_mcq_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='purpose',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='whizzo_app.purposemodel'),
        ),
    ]
