# Generated by Django 2.2.6 on 2020-01-15 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='classes',
            field=models.IntegerField(choices=[(1, '计算1班'), (2, '计算2班')], default=1, verbose_name='班级'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='gender',
            field=models.IntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别'),
        ),
    ]
