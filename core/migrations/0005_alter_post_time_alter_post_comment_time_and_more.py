# Generated by Django 4.1 on 2022-09-13 07:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_post_post_comment_post_video_post_share_post_like_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 13, 9, 14, 51, 647178)),
        ),
        migrations.AlterField(
            model_name='post_comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 13, 9, 14, 51, 651603)),
        ),
        migrations.AlterField(
            model_name='post_comment_reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 13, 9, 14, 51, 652744)),
        ),
    ]
