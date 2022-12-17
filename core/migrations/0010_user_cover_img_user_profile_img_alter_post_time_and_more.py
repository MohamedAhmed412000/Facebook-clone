# Generated by Django 4.1 on 2022-09-13 09:36

import core.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_user_cover_img_remove_user_profile_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cover_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to=core.models.Upload.upload_location),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to=core.models.Upload.upload_location),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 13, 11, 36, 54, 527195)),
        ),
        migrations.AlterField(
            model_name='post_comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 13, 11, 36, 54, 531772)),
        ),
        migrations.AlterField(
            model_name='post_comment_reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 13, 11, 36, 54, 533043)),
        ),
        migrations.DeleteModel(
            name='User_Imgs',
        ),
    ]
