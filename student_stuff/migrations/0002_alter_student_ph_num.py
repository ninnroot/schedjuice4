# Generated by Django 4.0.1 on 2022-01-25 18:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_stuff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='ph_num',
            field=models.CharField(default='', max_length=16, validators=[django.core.validators.RegexValidator('^\\d{1,11}$')]),
        ),
    ]