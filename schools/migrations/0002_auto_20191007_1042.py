# Generated by Django 2.2.4 on 2019-10-07 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feetype',
            name='class1',
            field=models.CharField(default='0.0', max_length=100),
        ),
        migrations.AddField(
            model_name='feetype',
            name='class2',
            field=models.CharField(default='0.0', max_length=100),
        ),
        migrations.AddField(
            model_name='feetype',
            name='class3',
            field=models.CharField(default='0.0', max_length=100),
        ),
    ]