# Generated by Django 3.0.6 on 2023-06-12 02:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialmediaapp', '0022_auto_20230612_0730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='friend',
        ),
        migrations.AddField(
            model_name='friend',
            name='friends',
            field=models.ManyToManyField(related_name='friendships_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
