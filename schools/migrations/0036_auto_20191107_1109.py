# Generated by Django 2.2.4 on 2019-11-07 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0035_auto_20191106_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlysalarypaid',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.School'),
        ),
    ]