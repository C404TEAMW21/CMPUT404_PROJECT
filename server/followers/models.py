from django.db import models

from main import models as mainModels
from author.serializers import AuthorProfileSerializer

class Follower(models.Model):
    # follow follows author
    # author is always going to be on our server
    author = models.ForeignKey(mainModels.Author, related_name="follower", on_delete=models.CASCADE)
    follower = models.JSONField()
    follower_id = models.CharField(max_length=40)

    class Meta:
        unique_together = ('author', 'follower_id')

class Following(models.Model):
    # author follows following
    # following is always going to be on our server
    author_id = models.CharField(max_length=40)
    following_id = models.CharField(max_length=40)

    class Meta:
        unique_together = ('author_id', 'following_id')
