# Generated by Django 3.0.6 on 2023-06-12 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmediaapp', '0024_auto_20230612_0738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='status',
        ),
    ]