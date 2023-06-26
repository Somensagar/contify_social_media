# Generated by Django 3.0.6 on 2023-05-23 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmediaapp', '0008_auto_20230524_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/'),
        ),
    ]
