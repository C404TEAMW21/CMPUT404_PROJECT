from rest_framework import serializers

from main import models
from author.serializers import AuthorProfileSerializer
class FollowersSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    
    def get_followers(self, obj):
        followersObj = obj.all().first()
        allFollowers = followersObj.followers.all()
        return [AuthorProfileSerializer(obj).data for obj in allFollowers]

    class Meta:
        model = models.Followers
        fields = ('followers',)

class FollowersModificationSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    
    def get_followers(self, obj):
        followersObj = obj.all().first()
        allFollowers = followersObj.followers.all()
        return allFollowers
        
    class Meta:
        model = models.Followers
        fields = ('followers',)
