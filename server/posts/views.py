import re

from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, authentication, permissions, mixins, status
from django.http import Http404
from django.core.paginator import Paginator
from rest_framework.response import Response

from main.models import Author, Followers
from .models import Post
from .serializers import PostSerializer
from inbox.models import Inbox


# service/author/{AUTHOR_ID}/posts/{POST_ID}
class UpdatePostView(generics.RetrieveUpdateDestroyAPIView): #mixins.DestroyModelMixin
    http_method_names = ['get', 'post', 'delete', 'put']
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # returns a post object with the matching author_id and pk (post_id)
    # returns 404 otherwise
    def get_post(self):
        pk = self.kwargs.get('')
        request_author_id = self.kwargs['author_id']
        request_post_id = self.kwargs['pk']

        # TODO: allow friends to view the post too
        if (self.request.user.id == request_author_id):
            a_post = get_object_or_404(Post, pk=request_post_id)
        else:
            a_post = get_object_or_404(Post, pk=request_post_id, visibility=Post.PUBLIC)
        return a_post

    # GET the post with the right author_id and post_id
    def retrieve(self, request, *args, **kwargs):
        a_post = self.get_post()
        return Response(PostSerializer(a_post).data)
    
    # DELETE - Only the author of the post can perform the deletion
    def delete(self, request, *args, **kwargs):
        if (self.kwargs['author_id'] != self.request.user.id):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if self.get_post():
            self.get_post().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Update this
            return Response(status=status.HTTP_404_NOT_FOUND)

    # POST - update existing post
    def post(self, request, *args, **kwargs):
        if (self.kwargs['author_id'] != self.request.user.id):  
            return Response(status=status.HTTP_403_FORBIDDEN)

        a_post = self.get_post()
        serializer = PostSerializer(a_post, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT - update existing or create a new post
    def update(self, request, *args, **kwargs):
        if (self.kwargs['author_id'] != self.request.user.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        instance = Post.objects.filter(id=self.kwargs['pk']).first()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if instance is None:
            self.perform_create(serializer, **kwargs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)


# service/author/{AUTHOR_ID}/posts/
class CreatePostView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        request_author_id = self.kwargs['author_id']

        # TODO: allow friends to view the post too
        try:
            if (self.request.user.id == request_author_id):
                queryset = Post.objects.filter(
                    author=Author.objects.get(id=self.request.user.id)
                ).order_by('-published')
            else:
                queryset = Post.objects.filter(
                    author=Author.objects.get(id=request_author_id),
                    visibility='PUBLIC'
                ).order_by('-published')
        except get_user_model().DoesNotExist:
            raise Http404

        return queryset
    
    # GET: Paginated posts
    # /service/author/<AUTHOR_ID>/posts?page=1&size=2
    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('size') or 20
        page = request.query_params.get('page') or 1
        posts = self.get_queryset() 
        paginator = Paginator(posts, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(PostSerializer(item).data)

        return Response(data)

    # POST: perform_create is called before saving to the database  
    def post(self, request, *args, **kwargs):
        author = Author.objects.get(id=self.kwargs['author_id'])
        if (author.id != self.request.user.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        post = self.create(request, *args, **kwargs)

        post_data = post.data
        try:
            followers = Followers.objects.get(author=author).followers.all()
        except Followers.DoesNotExist:
            return post
        # use re to match as DRF only returns id with host due to serializer
        post_id = re.match(r'.*/posts/([0-9a-f-]*)/', post_data['id'])
        if post_id == None:
            raise Exception('post id matching error.')

        if (post_data['visibility'] == Post.PUBLIC):
            for follower in followers:
                Inbox.objects.get(author=follower.id) \
                    .send_to_inbox(post_id.group(1))
        if (post_data['visibility'] == Post.FRIENDS):
            for follower in followers:
                if Followers.is_friends(self, follower, author):
                    Inbox.objects.get(author=follower.id) \
                        .send_to_inbox(post_id.group(1))
        return post
        
    def perform_create(self, serializer):
        request_author_id = self.request.user.id
        serializer.save(author=Author.objects.get(id=request_author_id))


# service/public/
class PublicPostView(generics.ListAPIView):
    serializer_class = PostSerializer

    # GET: get all public and not unlisted Post
    def get_queryset(self):
        queryset = Post.objects.filter(visibility=Post.PUBLIC, unlisted=False).order_by('-published')
        return queryset
    
    # GET: Paginated posts
    # service/public?page=1&size=2
    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('size') or 20
        page = request.query_params.get('page') or 1
        posts = self.get_queryset() 
        paginator = Paginator(posts, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(PostSerializer(item).data)

        return Response(data)


# service/author/{AUTHOR_ID}/posts/{POST_ID}/share
class SharePostView(generics.CreateAPIView):
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        sharer_id = request.data.get('from')
        if sharer_id == None:
            return Response({'error':'from is empty!'},
                            status=status.HTTP_400_BAD_REQUEST)
        post_id = self.kwargs['pk']
        share_to = request.data.get('share_to')
        if share_to:
            if share_to == 'all':
                try:
                    friend_list = Followers.objects.get(author=sharer_id) \
                        .friends()
                except Followers.DoesNotExist:
                    return Response({'data': f'No friends to share to'},
                                    status=status.HTTP_200_OK)

                for friend in friend_list:
                    try:
                        inbox = Inbox.objects.get(author=friend.id)
                        inbox.send_to_inbox(post_id)
                    except:
                        pass
                return Response({'data': f'Shared {post_id} with {share_to}'},
                                status=status.HTTP_200_OK)
            else:
                try:
                    Inbox.objects.get(author=share_to).send_to_inbox(post_id)
                except (Post.DoesNotExist, Inbox.DoesNotExist) as e:
                    return Response({'error': 'Post or Author not found!'},
                                    status=status.HTTP_404_NOT_FOUND)
                return Response({'data': f'Shared {post_id} with {share_to}'},
                                status=status.HTTP_200_OK)
        else:
            return Response({'error':'share_to is empty!'},
                            status=status.HTTP_400_BAD_REQUEST)
