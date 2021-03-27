from rest_framework import serializers
from .models import Like
from author.serializers import AuthorProfileSerializer

class LikeSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Like
        fields = ( 'type', 'author', 'object')
        read_only_fields = fields
