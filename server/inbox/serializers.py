from ast import literal_eval

from django.core.paginator import Paginator
from rest_framework import serializers

from main import utils
from .models import Inbox

class InboxSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('paginated_items')
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return f"{utils.HOST}/author/{obj.author.id}"

    def paginated_items(self, obj):
        data = []
        # Paginate Nested Object
        # From https://stackoverflow.com/a/49677960
        page_size = self.context['request'].query_params.get('size') or 10
        page = self.context['request'].query_params.get('page') or 1
        paginator = Paginator(obj.items, page_size)

        items = paginator.page(page)
        for item in items:
            data.append(item)
        return data

    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')