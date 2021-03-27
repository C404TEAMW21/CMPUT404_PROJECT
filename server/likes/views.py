from django.shortcuts import render
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework import generics, permissions

from .serializers import LikeSerializer
from .models import Like


# api/author/{author_id}/post/{post_id}/likes
class ListPostLikesView(generics.ListCreateAPIView):
    http_method_names = ['get']
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Like.objects.filter(
            object_type=Like.LIKE_POST,
            object_id=self.kwargs['post_id']
        ).order_by('id')
        return queryset

    # GET: Paginated likes for posts
    # api/author/{author_id}/post/{post_id}/likes?page=1&size=2
    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('size') or 20
        page = request.query_params.get('page') or 1
        posts = self.get_queryset() 
        paginator = Paginator(posts, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(LikeSerializer(item).data)

        return Response(data)

# api/author/{author_id}/post/{post_id}/comments/{comment_id}/likes
class ListCommentLikesView(generics.ListCreateAPIView):
    http_method_names = ['get']
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Like.objects.filter(
            object_type=Like.LIKE_COMMENT,
            object_id=self.kwargs['comment_id']
        ).order_by('id')
        return queryset

    # GET: Paginated likes for comments
    # api/author/{author_id}/post/{post_id}/comments/{comment_id}/likes?page=1&size=2
    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('size') or 20
        page = request.query_params.get('page') or 1
        posts = self.get_queryset() 
        paginator = Paginator(posts, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(LikeSerializer(item).data)

        return Response(data)

# api/author/{author_id}/liked
class ListLikedView(generics.RetrieveAPIView):
    http_method_names = ['get']
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Like.objects.filter(
            author_id=self.kwargs['author_id']
        ).order_by('id')
        return queryset
    
    def get(self, request, *args, **kwargs):
        liked_items = self.get_queryset()
        items = LikeSerializer(liked_items, many=True).data
        response = {
            'type': 'liked',
            'items': items
        }
        return Response(response)
