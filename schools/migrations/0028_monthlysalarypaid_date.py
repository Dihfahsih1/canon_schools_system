# Generated by Django 2.2.4 on 2019-10-28 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0027_monthlysalarypaid_employees_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlysalarypaid',
            name='date',
            field=models.DateField(auto_now_add=True, default='2019-10-28'),
            preserve_default=False,
        ),
    ]
