# Generated by Django 3.0.6 on 2023-06-13 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialmediaapp', '0034_auto_20230613_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='friends',
        ),
        migrations.AddField(
            model_name='friend',
            name='friend',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
