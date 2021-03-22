from rest_framework import serializers
from .models import Comment
from author.serializers import AuthorProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = AuthorProfileSerializer(obj.author).data
        return author
    
    def get_id(self, obj):
        return obj.get_id_url()       

    class Meta:
        model = Comment
        fields = (
            'type', 'id', 'author', 'comment', 'contentType', 'published'
        )
        read_only_fields = ['type', 'id', 'post', 'author', 'published']
