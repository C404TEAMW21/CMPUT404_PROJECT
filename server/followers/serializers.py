from rest_framework import serializers

from main import models
from author.serializers import AuthorProfileSerializer

class FollowersSerializer(serializers.ModelSerializer):
    followers = AuthorProfileSerializer(read_only=True, many=True)

    class Meta:
        model = models.Followers
        fields = ('followers',)

class FollowersModificationSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    

    def get_followers(self, obj):
        context = self.context
        request = context.get("request")
        qs = request

        return qs
    class Meta:
        model = models.Followers
        fields = ('followers',)   

class FollowersFriendSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()

    def get_friends(self, obj):
        friends = AuthorProfileSerializer(obj.friends(), many=True)
        return friends.data

    class Meta:
        model = models.Followers
        fields = ('friends',)
