from rest_framework import serializers
from .models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer
from author.serializers import AuthorProfileSerializer

class PostSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    recent_comments = serializers.SerializerMethodField()

    def get_count(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    def get_comments(self, obj):
        return obj.get_comments_page_url()
    
    def get_recent_comments(self, obj):
        # Gets the five recently published comment
        if (obj.visibility == Post.PUBLIC):
            queryset = Comment.objects.filter(post=obj).order_by('-published')[:5]
        else:
            queryset = []
        serializer = CommentSerializer(reversed(queryset), many=True)
        return serializer.data

    def get_author(self, obj):
        author = AuthorProfileSerializer(obj.author).data
        return author
    
    def get_id(self, obj):
        return obj.get_id_url()

    class Meta:
        model = Post
        fields = (
            'type', 'title', 'id', 'source', 'origin', 
            'description', 'contentType', 'content',
            'author', 'count', 'size', 'comments', 'recent_comments', 
            'published', 'visibility', 'unlisted', 'categories'
        )
        read_only_fields = ['type', 'id', 'author']
