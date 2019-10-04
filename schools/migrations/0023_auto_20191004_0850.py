# Generated by Django 2.2.4 on 2019-10-04 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0022_auto_20191003_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Classroom'),
        ),
        migrations.AddField(
            model_name='section',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Subject'),
        ),
        migrations.AlterField(
            model_name='feetype',
            name='fee_type',
            field=models.CharField(choices=[('Tuition', 'Tuition'), ('Hostel', 'Hostel'), ('Transport', 'Transport')], max_length=100),
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Classroom')),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Exam')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.School')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Section')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Subject')),
            ],
        ),
    ]