# Generated by Django 2.2.4 on 2019-10-24 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0026_delete_searchpaymenthistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlysalarypaid',
            name='employees_id',
            field=models.CharField(default='id', max_length=100),
        ),
    ]