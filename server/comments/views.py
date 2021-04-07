from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render

from .serializers import CommentSerializer
from .models import Comment
from posts.models import Post
from nodes.models import Node
from main.models import Author, Followers, Following
from inbox.models import Inbox
from rest_framework import generics, status
from rest_framework.response import Response
from main import utils
from urllib.parse import urlparse
import requests

# For creating Remote Comments
# <uuid:author_id>/posts/<uuid:post_id>/create_remote_comments
class CreateRemoteCommentView(generics.ListCreateAPIView):
    http_method_names = ['post']
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post_owner = self.kwargs['author_id']

        comments_url = request.data.get('comment_url')
        parsed_uri = urlparse(comments_url)
        object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        request.data['author']['id'] = f'{utils.HOST}/author/{str(self.request.user.id)}'
        try:
            remote_server = Node.objects.get(remote_server_url=object_host)
        except Node.DoesNotExist:
            return Response({'error':'Could not find specified remote server'}, status=status.HTTP_404_NOT_FOUND)

        r = requests.post(
                comments_url,
                json=request.data,
                auth=(remote_server.konnection_username, remote_server.konnection_password))

        return Response(r.json(), status=r.status_code)

# For getting Remote Comments
# <uuid:author_id>/posts/<uuid:post_id>/get_remote_comments
class GetRemoteCommentView(generics.ListCreateAPIView):
    http_method_names = ['post']
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post_owner = self.kwargs['author_id']

        comments_url = request.data.get('comment_url')
        parsed_uri = urlparse(comments_url)
        object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        try:
            remote_server = Node.objects.get(remote_server_url=object_host)
        except Node.DoesNotExist:
            return Response({'error':'Could not find specified remote server'}, status=status.HTTP_404_NOT_FOUND)

        r = requests.get(
                comments_url,
                auth=(remote_server.konnection_username, remote_server.konnection_password))

        return Response(r.json(), status=r.status_code)


# <uuid:author_id>/posts/<uuid:post_id>/comments
class CreateCommentView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post_owner = self.kwargs['author_id']
        request_user = self.request.user.id     # person doing GET
        queryset = []

        try:
            post = Post.objects.get(id=post_id)
            # if requesting user is the post owner
            #   OR it is a public post, then return all comments
            if (request_user == post_owner or post.visibility == Post.PUBLIC):
                queryset = Comment.objects.filter(post=post_id).order_by('published')

            # if it is a friend post, check if requesting user is a friend
            #   and return only comments between friend and author
            else:
                are_friends = False
                # remote user getting comments
                if self.request.user.type == 'node':
                    comments = Comment.objects.filter(
                        post=post_id, 
                    ).order_by('published')    

                    for comment in comments:
                        if (comment.author['id'] == str(post_owner) or 
                                comment.author['host'] == self.request.user.url):
                            queryset.append(comment)
                
                # local user getting comments
                else:
                    author = Author.objects.get(id=request_user)
                    local_friends = Following.get_all_local_friends(self, post_owner)
                    if author in local_friends:
                        are_friends = True
        
                if are_friends:
                    comments = Comment.objects.filter(
                        post=post_id, 
                    ).order_by('published')    

                    for comment in comments:
                        if (comment.author['id'] == str(request_user) or comment.author['id'] == str(post_owner)):
                            queryset.append(comment)
 
        except (Post.DoesNotExist, Comment.DoesNotExist, Author.DoesNotExist):
            raise Http404

        return queryset

    # GET: Paginated comments
    # /service/author/<uuid:author_id>/posts/<uuid:post_id>/comments?page=1&size=2
    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('size') or 20
        page = request.query_params.get('page') or 1
        comments = self.get_queryset()
        paginator = Paginator(comments, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(CommentSerializer(item).data)

        return Response(data)

    # POST: Add your comment to the post
    def post(self, request, *args, **kwargs):
        post_id = str(self.kwargs['post_id'])
        post_owner = str(self.kwargs['author_id'])
        
        try:
            request_user = str(self.request.data['author']['id'].split('/')[-1])
            comment_data = self.request.data['comment']
        except:
            return Response(
                {'error': "Need all mandatory keys: 'author' (with id), 'comment'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # post + post author is on our own server
        try:
            post = Post.objects.get(id=post_id)
            # if requesting user is the post owner
            #   OR it is a public post, then allow user to make a comment
            #   OR it is a friend post, and request_user is a friend of post_owner
            if (request_user == post_owner or post.visibility == Post.PUBLIC):
                comment = self.create(request, *args, **kwargs)
                return Response(comment.data, status=status.HTTP_201_CREATED)
            else:
                # remote user creating comments
                if self.request.user.type == 'node':
                    remote_friends = Following.get_all_remote_friends(self, post_owner).values()
                    remote_friend_ids = [friend.get('id') for friend in remote_friends]
                    if request_user in remote_friend_ids:
                        comment = self.create(request, *args, **kwargs)
                        return Response(comment.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(
                            {'error': 'The specified author id is not a friend'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                # local user creating comments
                else:
                    if request_user != str(self.request.user.id):
                        return Response(
                            {'error': 'You cannot make a comment for another person'},
                            status=status.HTTP_403_FORBIDDEN
                        )

                    local_friends = Following.get_all_local_friends(self, post_owner)
                    author = Author.objects.get(id=request_user)
                    if author in local_friends:
                        comment = self.create(request, *args, **kwargs)
                        return Response(comment.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(
                            {'error': 'The specified author id is not a friend'},
                            status=status.HTTP_403_FORBIDDEN
                        )
        except Post.DoesNotExist:
            msg = 'post does not exist'
        except Author.DoesNotExist:
            msg = 'author does not exist'

        return Response(
            {'error': msg},
            status=status.HTTP_404_NOT_FOUND
        )

    # Called during POST, before saving comment to the database
    def perform_create(self, serializer, **kwargs):
        request_author = self.request.data['author'] # person doing POST
        serializer.save(
            author=request_author,
            post=Post.objects.get(id=self.kwargs.get('post_id')),
        )
