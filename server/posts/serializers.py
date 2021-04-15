from rest_framework import serializers
from .models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer
from author.serializers import AuthorProfileSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    def get_size(self, obj):
        return 20 # default page size
    
    def get_comments(self, obj):
        return obj.get_comments_page_url()

    def get_author(self, obj):
        author = AuthorProfileSerializer(obj.author).data
        return author

    class Meta:
        model = Post
        fields = (
            'type', 'title', 'id', 'source', 'origin', 
            'description', 'contentType', 'content',
            'author', 'count', 'size', 'comments',
            'published', 'visibility', 'unlisted', 'categories'
        )
        read_only_fields = ['type', 'id', 'author']
