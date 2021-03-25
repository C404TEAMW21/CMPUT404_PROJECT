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
        remote = Followers.objects.get(author=author).remoteFollowers  
        allAuthorList = []
        for key, value in remote.items():
            allAuthorList.extend(value.values())
    
        return allAuthorList
    # TODO: Delete this function 
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
    # TODO: Delete this function 
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
    remoteFollowing = models.JSONField(default=dict)

    def get_all_local_following(self, author):
        return Following.objects.get(author=author).following.all()

    def get_all_remote_following(self, author):
        return Following.objects.get(author=author).remoteFollowing  

    def get_all_local_friends(self, author):
        return Followers.objects.get(author=author).followers.all() & Following.objects.get(author=author).following.all()

    def get_all_remote_friends(self, author):
        remote_followers_obj = Followers.objects.get(author=author).remoteFollowers.values()
        remote_followering_obj = Following.objects.get(author=author).remoteFollowing.values()
        remote_follower_list = []
        remote_following_list = []
        friends_list = []
        for follower in remote_followers_obj:
            remote_follower_list.extend(follower.keys())

        for following in remote_followering_obj:
            remote_following_list.extend(following.keys())
       
        friends = list( set(remote_follower_list) & set(remote_following_list))
        
        for friend in friends:
            for i in remote_followering_obj:
                friends_list.append(i[friend])
    
        return friends_list

    
      
