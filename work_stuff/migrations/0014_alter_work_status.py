# Generated by Django 4.0.1 on 2022-02-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_stuff', '0013_remove_session_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='status',
            field=models.CharField(default='pending', max_length=32),
        ),
    ]
