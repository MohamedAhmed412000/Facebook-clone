from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from datetime import datetime as dt

# This to get django user model
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Upload:
    def __init__(self, name):
        self.name = name

    def upload_location(self, instance, filename):
        return f'user/{instance.id}/{self.name}/{filename}'

    def upload_post_location(self, instance, filename):
        return f'user/{instance.post.user.id}/{self.name}/{filename}'
    
privacy_choices = (
        (0, 'Public'),
        (1, 'Friends'),
        (2, 'Only me'),
    )

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    birth = models.DateField(default=dt(2000, 1, 1).date())
    is_male = models.BooleanField(default=True)
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to=Upload('profile_images').upload_location, default="blank-profile-picture.png")
    cover_img = models.ImageField(upload_to=Upload('cover_images').upload_location, default="default-cover.png")
    location = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=11, default='', unique=True)
    job = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=6, default='0')
    privacy = models.IntegerField(default=1, choices=privacy_choices)
    friends_privacy = models.IntegerField(default=1, choices=privacy_choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class User_Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class Tag(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    time = models.DateTimeField(default=dt.now())
    privacy = models.IntegerField(default=0, choices=privacy_choices)
    has_img = models.BooleanField(default=False)
    has_vid = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    shared_post = models.ForeignKey('Post', on_delete=models.SET_NULL, related_name='actual_post', null=True)
    num_of_likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    num_of_comments = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    num_of_shares = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    disable_comments = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} add Post'

class Post_Tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name

class Post_Img(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=Upload('posts_images').upload_post_location)

    def __str__(self):
        return self.img.path.split('/')[-1]
    
class Post_Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vid = models.FileField(upload_to=Upload('posts_videos').upload_post_location)

    def __str__(self):
        return self.vid.path.split('/')[-1]

class Post_Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} likes {self.post}'
    
class Post_Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    time = models.DateTimeField(default=dt.now())
    likes_num = models.IntegerField(default=0)
    has_reply = models.BooleanField(default=False)
    has_img = models.BooleanField(default=False)
    has_vid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user} comments on {self.post}'

class Comment_Img(models.Model):
    comment = models.ForeignKey(Post_Comment, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to=Upload('comment_images').upload_post_location)

    def __str__(self):
        return self.img.path.split('/')[-1]

class Comment_Vid(models.Model):
    comment = models.ForeignKey(Post_Comment, on_delete=models.SET_NULL, null=True)
    vid = models.FileField(upload_to=Upload('comment_videos').upload_post_location)

    def __str__(self):
        return self.vid.path.split('/')[-1]

class Post_Comment_Reply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    comment = models.ForeignKey(Post_Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    time = models.DateTimeField(default=dt.now())
    likes_num = models.IntegerField(default=0)
    has_img = models.BooleanField(default=False)
    has_vid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user} replies on {self.comment}'

class Followship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    time = models.DateTimeField(default=dt.now())
    
    def __str__(self):
        return f'{self.follower} follows {self.user}'
    
