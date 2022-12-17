# Generated by Django 4.1 on 2022-09-14 09:28

import core.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_user_job_remove_user_phone_alter_post_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 11, 28, 39, 778783)),
        ),
        migrations.AlterField(
            model_name='post_comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 11, 28, 39, 783915)),
        ),
        migrations.AlterField(
            model_name='post_comment_reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 11, 28, 39, 785234)),
        ),
        migrations.AlterField(
            model_name='user',
            name='cover_img',
            field=models.ImageField(default='default-cover.png', upload_to=core.models.Upload.upload_location),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to=core.models.Upload.upload_location),
        ),
    ]
