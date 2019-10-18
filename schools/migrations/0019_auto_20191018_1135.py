# Generated by Django 2.2.4 on 2019-10-18 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0018_remove_salarypayment_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarypayment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='salarypayment',
            name='teacher',
        ),
        migrations.AddField(
            model_name='salarypayment',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Employee'),
        ),
    ]
