# Generated by Django 4.1 on 2022-09-14 09:19

import core.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_post_time_alter_post_comment_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 11, 19, 13, 107477)),
        ),
        migrations.AlterField(
            model_name='post_comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 11, 19, 13, 112323)),
        ),
        migrations.AlterField(
            model_name='post_comment_reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 11, 19, 13, 113536)),
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
