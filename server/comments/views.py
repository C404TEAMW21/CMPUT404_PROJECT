from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render

from .serializers import CommentSerializer
from .models import Comment
from posts.models import Post
from main.models import Author, Followers
from rest_framework import generics, status
from rest_framework.response import Response


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
                author1 = Author.objects.get(id=request_user)
                author2 = Author.objects.get(id=post_owner)
                if author1 and author2 and Followers.is_friends(self, author1, author2):
                    queryset = Comment.objects.filter(
                        post=post_id, 
                        author__in = (post_owner, request_user)
                    ).order_by('published')    
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
        post_id = self.kwargs['post_id']
        post_owner = self.kwargs['author_id']
        request_user = self.request.user.id     # person doing POST
        
        try:
            post = Post.objects.get(id=post_id)
            commenter = Author.objects.get(id=request_user)

            # if requesting user is the post owner
            #   OR it is a public post, then allow user to make a comment
            #   OR it is a friend post, and request_user is a friend of post_owner
            if (request_user == post_owner or post.visibility == Post.PUBLIC):
                comment = self.create(request, *args, **kwargs)
            else:
                author1 = Author.objects.get(id=request_user)
                author2 = Author.objects.get(id=post_owner)
                if author1 and author2 and Followers.is_friends(self, author1, author2):
                    comment = self.create(request, *args, **kwargs)
                    return comment

                return Response(status=status.HTTP_403_FORBIDDEN)

        except (Post.DoesNotExist, Comment.DoesNotExist):
            raise Http404
        except Author.DoesNotExist:
            raise Http404

        return Response(comment.data, status=status.HTTP_201_CREATED)

    # Called during POST, before saving comment to the database
    def perform_create(self, serializer, **kwargs):
        request_author_id = self.request.user.id # person doing POST
        serializer.save(
            author=Author.objects.get(id=request_author_id),
            post=Post.objects.get(id=self.kwargs.get('post_id')),
        )
