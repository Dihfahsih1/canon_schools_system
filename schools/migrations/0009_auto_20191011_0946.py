# Generated by Django 2.2.4 on 2019-10-11 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0008_auto_20191011_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='fee_amount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fee_am', to='schools.FeeType'),
        ),
    ]