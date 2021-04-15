from django.core.paginator import Paginator
from rest_framework import serializers

from main import utils
from .models import Inbox


class InboxSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('paginated_items')
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return f"{utils.FRONTEND_HOST}/author/{obj.author.id}"

    def paginated_items(self, obj):
        data = []
        page_size = self.context['request'].query_params.get('size') or 50
        page = self.context['request'].query_params.get('page') or 1
        paginator = Paginator(obj.items, page_size)

        items = paginator.page(page)
        for item in items:
            data.append(item)
        return data

    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')
