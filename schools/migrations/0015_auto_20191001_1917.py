# Generated by Django 2.2.4 on 2019-10-01 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0014_complain_action_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manageuser',
            old_name='school',
            new_name='school_name',
        ),
        migrations.RenameField(
            model_name='manageuser',
            old_name='user',
            new_name='user_details',
        ),
    ]