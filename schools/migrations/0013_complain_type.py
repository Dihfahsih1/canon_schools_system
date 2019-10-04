# Generated by Django 2.2.4 on 2019-10-01 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0012_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain_type', models.CharField(max_length=100)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.School')),
            ],
        ),
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain_date', models.DateField(null=True)),
                ('complain', models.TextField(max_length=400)),
                ('complain_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Type')),
                ('complain_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('complain_user_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Role')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.School')),
            ],
        ),
    ]