from django.db import models

from main import models as mainModels
from author.serializers import AuthorProfileSerializer

class FriendRequest(models.Model):
    type = 'Follow'
    
    author = models.ForeignKey(mainModels.Author, on_delete=models.CASCADE, related_name='follower')
    follower = models.ForeignKey(mainModels.Author, on_delete=models.CASCADE, related_name='author')

    class Meta:
        unique_together = ('author', 'follower',)

    def summary(self):
        return f"{self.follower.username} wants to follow {self.author.username}"

    # actor is the follower
    def actor(self): 
        return AuthorProfileSerializer(self.follower).data
    
    def object(self):
        return AuthorProfileSerializer(self.author).data