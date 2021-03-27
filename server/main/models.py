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
        author = self.model(username=re.sub(r'\W+', '', username), **extra_fields)
        author.set_password(password)
        author.url = f'{utils.FRONTEND_HOST}/author/{author.id}'
        author.save(using=self._db)

        return author

    def create_superuser(self, username, password):
        user=self.create_author(username, password)
        user.is_superuser=True
        user.is_staff=True
        user.type=utils.UserType.superuser.value
        user.save(using=self._db)

        return user


class Author(AbstractBaseUser, PermissionsMixin):
    # Required objects
    type=models.CharField(max_length=25, default=utils.UserType.author.value)
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host=models.CharField(max_length=253, default=utils.HOST)
    displayName=models.CharField(max_length=255, blank=True)
    url= models.CharField(max_length=255, default='')
    github=models.CharField(max_length=255, default='', blank=True)
    
    adminApproval = models.BooleanField(default=False)
    username = models.CharField(max_length=25, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_id_url(self):
        return f'{utils.FRONTEND_HOST}/author/{str(self.id)}'

class Followers(models.Model):
    author = models.ForeignKey(Author, related_name="followers", on_delete=models.CASCADE)
    followers = models.ManyToManyField(Author, related_name='author_followers')
    remoteFollowers = models.JSONField(default=dict)

    def get_all_local_followers(self, author):
        return Followers.objects.get(author=author).followers.all()

    def get_all_remote_followers(self, author):
        return Followers.objects.get(author=author).remoteFollowers  
        

    def friends(self):
        list = []
        for author in self.followers.all():
            try:
                object = Followers.objects.get(author=author)
                if self.author in object.followers.all():
                    list.append(author)
            except Followers.DoesNotExist:
                pass
        return list
    
    def is_friends(self, author1, author2):
        try:
            author1_followers = Followers.objects.get(author=author1).followers.all()
            author2_followers = Followers.objects.get(author=author2).followers.all()
            if (author1 in author2_followers) and (author2 in author1_followers):
                return True
        except Followers.DoesNotExist:
            pass
        return False

class Following(models.Model):
    author = models.ForeignKey(Author, related_name="following", unique=False, on_delete=models.CASCADE)
    following = models.ManyToManyField(Author, related_name='author_following')
    remoteFollowering = models.JSONField(default=dict)


# create Inbox object after Author is created and called save()
@receiver(post_save, sender=Author)
def my_handler(sender, instance, **kwargs):
    if not Followers.objects.filter(author=instance).exists():
        Followers.objects.create(author=instance)
    if not Following.objects.filter(author=instance).exists():
        Following.objects.create(author=instance)