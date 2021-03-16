from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    