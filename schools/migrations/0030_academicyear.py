# Generated by Django 2.2.4 on 2019-10-29 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0029_employee_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Year')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.School')),
            ],
        ),
    ]