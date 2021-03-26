from django.db import models

from main import models as mainModels
from author.serializers import AuthorProfileSerializer

class Follower(models.Model):
    author = models.ForeignKey(mainModels.Author, related_name="followers", on_delete=models.CASCADE)
    follower = models.JSONField()
    follower_id = models.CharField(max_length=40)

    class Meta:
        unique_together = ('author', 'follower_id')
