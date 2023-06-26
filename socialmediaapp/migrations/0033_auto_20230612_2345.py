# Generated by Django 3.0.6 on 2023-06-12 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialmediaapp', '0032_auto_20230612_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='friends',
        ),
        migrations.AddField(
            model_name='friend',
            name='friend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friend',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='friend',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships', to=settings.AUTH_USER_MODEL),
        ),
    ]