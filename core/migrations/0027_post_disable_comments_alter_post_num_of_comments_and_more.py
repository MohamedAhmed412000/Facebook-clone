# Generated by Django 4.1 on 2022-09-28 15:02

import core.models
import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_post_num_of_comments_post_num_of_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='disable_comments',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='num_of_comments',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='num_of_likes',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='num_of_shares',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 28, 17, 2, 14, 38050)),
        ),
        migrations.AlterField(
            model_name='post_comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 28, 17, 2, 14, 44290)),
        ),
        migrations.AlterField(
            model_name='post_comment_reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 28, 17, 2, 14, 45530)),
        ),
        migrations.AlterField(
            model_name='post_img',
            name='img',
            field=models.ImageField(upload_to=core.models.Upload.upload_post_location),
        ),
        migrations.AlterField(
            model_name='post_video',
            name='vid',
            field=models.FileField(upload_to=core.models.Upload.upload_post_location),
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
