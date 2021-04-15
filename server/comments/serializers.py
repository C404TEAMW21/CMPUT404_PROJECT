from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        return obj.get_id_url()       

    class Meta:
        model = Comment
        fields = (
            'type', 'id', 'author', 'comment', 'contentType', 'published'
        )
        read_only_fields = ['type', 'id', 'post', 'author', 'published']
