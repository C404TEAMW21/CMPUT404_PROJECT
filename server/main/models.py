from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid
import re
from main import utils


class UserManager(BaseUserManager):
    def create_author(self, username, password, **extra_fields):
        author = self.model(username=re.sub(
            r'\W+', '', username), **extra_fields)
        author.set_password(password)
        author.url = f'{utils.FRONTEND_HOST}/author/{author.id}'
        author.save(using=self._db)

        return author

    def create_superuser(self, username, password):
        user = self.create_author(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.type = utils.UserType.superuser.value
        user.save(using=self._db)

        return user


class Author(AbstractBaseUser, PermissionsMixin):
    # Required objects
    type = models.CharField(max_length=25, default=utils.UserType.author.value)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=253, default=utils.HOST)
    displayName = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, default='')
    github = models.CharField(max_length=255, default='', blank=True)

    adminApproval = models.BooleanField(default=True)
    username = models.CharField(max_length=25, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        if not self.displayName:
            self.displayName = self.username
        super(Author, self).save(*args, **kwargs)

    def get_id_url(self):
        return f'{utils.FRONTEND_HOST}/author/{str(self.id)}'


class Followers(models.Model):
    author = models.ForeignKey(
        Author, related_name="followers", on_delete=models.CASCADE)
    followers = models.ManyToManyField(Author, related_name='author_followers')
    remoteFollowers = models.JSONField(default=dict)

    def get_all_local_followers(self, author):
        return Followers.objects.get(author=author).followers.all()

    def get_all_remote_followers(self, author):
        return Followers.objects.get(author=author).remoteFollowers


class Following(models.Model):
    author = models.ForeignKey(
        Author, related_name="following", on_delete=models.CASCADE)
    following = models.ManyToManyField(Author, related_name='author_following')
    remote_following = models.JSONField(default=dict)

    def get_all_local_following(self, author):
        return Following.objects.get(author=author).following.all()

    def get_all_remote_following(self, author):
        return Following.objects.get(author=author).remote_following

    def get_all_local_friends(self, author):
        return Followers.objects.get(author=author).followers.all() & Following.objects.get(author=author).following.all()

    def get_all_remote_friends(self, author):
        remote_followers = Followers.objects.get(author=author).remoteFollowers
        remote_following = Following.objects.get(author=author).remote_following
        friends_key = remote_followers.keys() & remote_following.keys()

        return {k: remote_following[k] for k in friends_key & remote_followers.keys()}

# create Follower and Following object after Author is created 
@receiver(post_save, sender=Author)
def my_handler(sender, instance, **kwargs):
    if not Followers.objects.filter(author=instance).exists():
        Followers.objects.create(author=instance)
    if not Following.objects.filter(author=instance).exists():
        Following.objects.create(author=instance)
