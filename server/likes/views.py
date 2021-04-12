from django.shortcuts import render
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework import generics, permissions, status

from .serializers import LikeSerializer
from .models import Like
from nodes.models import Node
from urllib.parse import urlparse
import requests

# api/author/{author_id}/post/{post_id}/likes
class ListPostLikesView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']
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
        page_size = request.query_params.get('size') or 50
        page = request.query_params.get('page') or 1
        posts = self.get_queryset() 
        paginator = Paginator(posts, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(LikeSerializer(item).data)

        return Response({'type': 'likes', 'items': data})
    
    # for getting likes for remote_post (requires 'post_url' in the body)
    def post(self, request, *args, **kwargs):
        post_url = request.data.get('post_url')
        if post_url == None:
            return Response({'error': 'Getting remote likes requires post_url in the body'}, status=status.HTTP_400_BAD_REQUEST)

        parsed_uri = urlparse(post_url)
        object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        post_owner = self.kwargs['author_id']
        post_id = self.kwargs['post_id']
        if 'team6' in object_host:
            likes_url = f"{object_host}author/{post_owner}/post/{post_id}/likes"
        else:
            likes_url = f"{object_host}api/author/{post_owner}/posts/{post_id}/likes"
        
        try:
            remote_server = Node.objects.get(remote_server_url=object_host)
        except Node.DoesNotExist:
            return Response({'error':'Could not find specified remote server'}, status=status.HTTP_404_NOT_FOUND)

        r = requests.get(
                likes_url,
                auth=(remote_server.konnection_username, remote_server.konnection_password)
            )

        # Find the likes locally
        if r.status_code < 200 or r.status_code >= 300:
            res = Like.objects.filter(object_id=post_id)
            res = LikeSerializer(res, many=True)
            res = {'type': 'likes', 'items': res.data}
            return Response(res, status=status.HTTP_200_OK)

        # If the output is a list
        res = r.json()
        if isinstance(res, list):
            res = {'type': 'likes', 'items': res}
        
        return Response(res, status=r.status_code)

# api/author/{author_id}/post/{post_id}/comments/{comment_id}/likes
class ListCommentLikesView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']
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
        page_size = request.query_params.get('size') or 50
        page = request.query_params.get('page') or 1
        posts = self.get_queryset() 
        paginator = Paginator(posts, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(LikeSerializer(item).data)

        return Response({'type': 'likes', 'items': data})
    
    # for getting likes for remote_comment (requires 'comment_url' in the body)
    def post(self, request, *args, **kwargs):
        comment_url = request.data.get('comment_url')
        if comment_url == None:
            return Response({'error': 'Getting remote likes requires comment_url in the body'}, status=status.HTTP_400_BAD_REQUEST)

        parsed_uri = urlparse(comment_url)
        object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        post_owner = self.kwargs['author_id']
        post_id = self.kwargs['post_id']
        comment_id = self.kwargs['comment_id']

        if 'team6' in object_host:
            likes_url = f"{object_host}author/{post_owner}/post/{post_id}/comments/{comment_id}/likes"
        else:
            likes_url = f"{object_host}api/author/{post_owner}/posts/{post_id}/comments/{comment_id}/likes"
        
        try:
            remote_server = Node.objects.get(remote_server_url=object_host)
        except Node.DoesNotExist:
            return Response({'error':'Could not find specified remote server'}, status=status.HTTP_404_NOT_FOUND)

        r = requests.get(
                likes_url,
                auth=(remote_server.konnection_username, remote_server.konnection_password)
            )

        # Find the likes locally
        if r.status_code < 200 or r.status_code >= 300:
            res = Like.objects.filter(object_id=comment_id)
            res = LikeSerializer(res, many=True)
            res = {'type': 'likes', 'items': res.data}
            return Response(res, status=status.HTTP_200_OK)
        
        # If the output is a list
        res = r.json()
        if isinstance(res, list):
            res = {'type': 'likes', 'items': res}
        
        return Response(res, status=r.status_code)

# api/author/{author_id}/liked
class ListLikedView(generics.RetrieveAPIView):
    http_method_names = ['get', 'post']
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Like.objects.filter(
            author_id=self.kwargs['author_id']
        ).order_by('id')
        return queryset
    
    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('size') or 50
        page = request.query_params.get('page') or 1
        posts = self.get_queryset() 
        paginator = Paginator(posts, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(LikeSerializer(item).data)

        return Response({'type': 'liked', 'items': data})
    
    # for getting liked for a remote author (requires 'host_url' in the body)
    def post(self, request, *args, **kwargs):
        host_url = request.data.get('host_url')
        if host_url == None:
            return Response({'error': 'Getting remote liked requires host_url in the body'}, status=status.HTTP_400_BAD_REQUEST)

        parsed_uri = urlparse(host_url)
        object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        post_owner = self.kwargs['author_id']
        if 'team6' in object_host:
            liked_url = f"{object_host}author/{post_owner}/liked"
        else:
            liked_url = f"{object_host}api/author/{post_owner}/liked"
        
        try:
            remote_server = Node.objects.get(remote_server_url=object_host)
        except Node.DoesNotExist:
            return Response({'error':'Could not find specified remote server'}, status=status.HTTP_404_NOT_FOUND)

        r = requests.get(
                liked_url,
                auth=(remote_server.konnection_username, remote_server.konnection_password)
            )
        
        # If the output is a list
        res = r.json()
        if isinstance(res, list):
            res = {'type': 'likes', 'items': res}
        
        return Response(res, status=r.status_code)
