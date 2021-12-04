# Generated by Django 3.2.9 on 2021-11-30 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff_stuff', '0002_staff_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(default='Description...')),
                ('color', models.CharField(default='#000000', max_length=7)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['id'], 'verbose_name': 'department', 'verbose_name_plural': 'departments'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'ordering': ['id'], 'verbose_name': 'staff', 'verbose_name_plural': 'staff members'},
        ),
        migrations.CreateModel(
            name='StaffTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff_stuff.tag')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
