from rest_framework import serializers

from .models import Follower
from author.serializers import AuthorProfileSerializer

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('author', 'follower')

