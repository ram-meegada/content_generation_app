# Generated by Django 4.2.11 on 2024-05-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whizzo_app', '0042_usermodel_country_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='abilitymodel',
            name='corect_answer',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='abilitymodel',
            name='is_mcq',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='achievementmodel',
            name='corect_answer',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='achievementmodel',
            name='is_mcq',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='categorymodel',
            name='sub_category',
            field=models.IntegerField(choices=[(1, 'QUESTIONS WITH OPTIONS'), (2, 'FLASH CARDS'), (3, 'ABILITIES'), (4, 'ACHIEVEMENTS'), (5, 'UPLOAD FILES OR BOOKS'), (6, 'NEW NOTE'), (7, 'WRITE ABOUT ME'), (8, 'NEW RESEARCH'), (9, 'UPLOAD REFERENCE'), (10, 'PDF TO WORD'), (11, 'WORD TO PDF'), (12, 'PDF TO JPEG'), (13, 'JPEG TO PDF'), (14, 'PDF TO EXCEL'), (15, 'EXCEL TO PDF'), (16, 'PDF TO PPT'), (17, 'PPT TO PDF')], default=0),
        ),
        migrations.AlterField(
            model_name='filesumarizationmodel',
            name='sub_category',
            field=models.IntegerField(choices=[(1, 'QUESTIONS WITH OPTIONS'), (2, 'FLASH CARDS'), (3, 'ABILITIES'), (4, 'ACHIEVEMENTS'), (5, 'UPLOAD FILES OR BOOKS'), (6, 'NEW NOTE'), (7, 'WRITE ABOUT ME'), (8, 'NEW RESEARCH'), (9, 'UPLOAD REFERENCE'), (10, 'PDF TO WORD'), (11, 'WORD TO PDF'), (12, 'PDF TO JPEG'), (13, 'JPEG TO PDF'), (14, 'PDF TO EXCEL'), (15, 'EXCEL TO PDF'), (16, 'PDF TO PPT'), (17, 'PPT TO PDF')], default=0),
        ),
        migrations.AlterField(
            model_name='notemodel',
            name='sub_category',
            field=models.IntegerField(choices=[(1, 'QUESTIONS WITH OPTIONS'), (2, 'FLASH CARDS'), (3, 'ABILITIES'), (4, 'ACHIEVEMENTS'), (5, 'UPLOAD FILES OR BOOKS'), (6, 'NEW NOTE'), (7, 'WRITE ABOUT ME'), (8, 'NEW RESEARCH'), (9, 'UPLOAD REFERENCE'), (10, 'PDF TO WORD'), (11, 'WORD TO PDF'), (12, 'PDF TO JPEG'), (13, 'JPEG TO PDF'), (14, 'PDF TO EXCEL'), (15, 'EXCEL TO PDF'), (16, 'PDF TO PPT'), (17, 'PPT TO PDF')], default=0),
        ),
        migrations.AlterField(
            model_name='reseaerchmodel',
            name='sub_category',
            field=models.IntegerField(choices=[(1, 'QUESTIONS WITH OPTIONS'), (2, 'FLASH CARDS'), (3, 'ABILITIES'), (4, 'ACHIEVEMENTS'), (5, 'UPLOAD FILES OR BOOKS'), (6, 'NEW NOTE'), (7, 'WRITE ABOUT ME'), (8, 'NEW RESEARCH'), (9, 'UPLOAD REFERENCE'), (10, 'PDF TO WORD'), (11, 'WORD TO PDF'), (12, 'PDF TO JPEG'), (13, 'JPEG TO PDF'), (14, 'PDF TO EXCEL'), (15, 'EXCEL TO PDF'), (16, 'PDF TO PPT'), (17, 'PPT TO PDF')], default=0),
        ),
    ]
