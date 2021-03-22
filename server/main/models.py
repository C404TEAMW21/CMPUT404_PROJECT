from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

import uuid
import re
from main import utils

class UserManager(BaseUserManager):
    def create_author(self, username, password, **extra_fields):
        author = self.model(username=re.sub(r'\W+', '', username), **extra_fields)
        author.set_password(password)
        author.url = f'{utils.HOST}/author/{author.id}'
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
        return f'{utils.HOST}/author/{str(self.id)}'

class Followers(models.Model):
    author = models.ForeignKey(Author, related_name="followers", on_delete=models.CASCADE)
    followers = models.ManyToManyField(Author, related_name='author_followers')
   

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following", unique=False, on_delete=models.CASCADE)
    following = models.ManyToManyField(Author, related_name='author_following')
