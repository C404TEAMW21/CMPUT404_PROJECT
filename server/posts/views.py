import requests, json, uuid

from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions, status
from django.http import Http404
from django.core.paginator import Paginator
from rest_framework.response import Response

from main.models import Author, Followers, Following
from nodes.models import Node
from .models import Post
from .serializers import PostSerializer
from inbox.models import Inbox


# api/author/{AUTHOR_ID}/posts/{POST_ID}
class UpdatePostView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'post', 'delete', 'put']
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post_from_inbox(self, sharer_id, request_post_id):
        try:
            sharer_items = Inbox.objects.get(author=sharer_id).items
        except Inbox.DoesNotExist:
            raise Http404
        for item in sharer_items:
            try:
                item_id = item['id']
            except KeyError:
                continue
            if request_post_id in item_id:
                return item
        raise Http404

    # returns a post object with the matching author_id and pk (post_id)
    # returns 404 otherwise
    def get_post(self):
        pk = self.kwargs.get('')
        request_author_id = uuid.UUID(self.kwargs['author_id'])
        request_post_id = self.kwargs['pk']
        sharer_id = self.request.user.id
        try:
            a_post = Post.objects.get(pk=uuid.UUID(request_post_id))
        except Post.DoesNotExist:
            return self.post_from_inbox(sharer_id, request_post_id)

        if (self.request.user.id != request_author_id):
            # if Friend Post, check if logged in user is a friend before giving Post
            if (a_post.visibility == Post.FRIENDS):
                local_friends = Following.get_all_local_friends(self, request_author_id)
                local_friend_ids = [str(friend.id) for friend in local_friends]
                remote_friends = Following.get_all_remote_friends(self, request_author_id).values()
                remote_friend_ids = [friend.get('id') for friend in remote_friends]
                request_id = str(self.request.user.id)
                if request_id not in local_friend_ids and request_id not in remote_friend_ids:
                    return self.post_from_inbox(sharer_id, request_post_id)   
        return a_post

    # GET the post with the right author_id and post_id
    def retrieve(self, request, *args, **kwargs):
        a_post = self.get_post()
        if isinstance(a_post, dict):
            return Response(a_post)
        else:
            return Response(PostSerializer(a_post).data)        
    
    # DELETE - Only the author of the post can perform the deletion
    def delete(self, request, *args, **kwargs):
        request_author_id = uuid.UUID(self.kwargs['author_id'])
        if (request_author_id != self.request.user.id):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if self.get_post():
            self.get_post().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Update this
            return Response(status=status.HTTP_404_NOT_FOUND)

    # POST - update existing post
    def post(self, request, *args, **kwargs):
        request_author_id = uuid.UUID(self.kwargs['author_id'])
        if (request_author_id != self.request.user.id):  
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
        request_author_id = uuid.UUID(self.kwargs['author_id'])
        post_id = uuid.UUID(self.kwargs['pk'])
        if (request_author_id != self.request.user.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        instance = Post.objects.filter(id=post_id).first()
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


# api/author/{AUTHOR_ID}/posts/
class CreatePostView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        request_author_id = self.kwargs['author_id']

        try:
            if (self.request.user.id == request_author_id):
                queryset = Post.objects.filter(
                    author=Author.objects.get(id=self.request.user.id),
                    unlisted=False
                ).order_by('-published')
            else:
                queryset = Post.objects.filter(
                    author=Author.objects.get(id=request_author_id),
                    unlisted=False
                ).order_by('-published')
                
                # if logged user is not a friend of AUTHOR_ID, return only public posts
                local_friends = Following.get_all_local_friends(self, request_author_id)
                local_friend_ids = [str(friend.id) for friend in local_friends]
                remote_friends = Following.get_all_remote_friends(self, request_author_id).values()
                remote_friend_ids = [friend.get('id') for friend in remote_friends]

                request_id = str(self.request.user.id)
                if request_id not in local_friend_ids and request_id not in remote_friend_ids:
                    queryset = queryset.filter(visibility=Post.PUBLIC)                

        except get_user_model().DoesNotExist:
            raise Http404

        return queryset
    
    # GET: Paginated posts
    # /api/author/<AUTHOR_ID>/posts?page=1&size=2
    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('size') or 50
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

        if (post_data['visibility'] == Post.PUBLIC):
            local_followers = Followers.get_all_local_followers(self, author.id)
            remote_followers = Followers.get_all_remote_followers(self, author.id).values()

            for follower in local_followers:
                try:
                    Inbox.objects.get(author=follower.id).send_to_inbox(post_data)
                except:
                    pass
            for follower in remote_followers:
                host_name = follower['host']
                if host_name[-1] == '/':
                    url = f"{follower['host']}api/author/{follower['id']}/inbox/"
                else:
                    host_name = follower['host'] + '/'
                    url = f"{follower['host']}/api/author/{follower['id']}/inbox/"
                if "team6" in host_name:
                    url = f"{host_name}author/{follower['id']}/inbox"
                try:
                    remote_server = Node.objects.get(remote_server_url=host_name)
                    req = requests.post(url,
                                        json=post_data,
                                        auth=(remote_server.konnection_username,
                                              remote_server.konnection_password))
                except Node.DoesNotExist:
                    pass

        if (post_data['visibility'] == Post.FRIENDS):
            local_friends = Following.get_all_local_friends(self, author.id)
            remote_friends = Following.get_all_remote_friends(self, author.id).values()

            for friend in local_friends:
                try:
                    Inbox.objects.get(author=friend.id).send_to_inbox(post_data)
                except:
                    pass
            for friend in remote_friends:
                host_name = friend['host']
                if host_name[-1] == '/':
                    url = f"{friend['host']}api/author/{friend['id']}/inbox/"
                else:
                    host_name = friend['host'] + '/'
                    url = f"{friend['host']}/api/author/{friend['id']}/inbox/"
                if "team6" in host_name:
                    url = f"{host_name}author/{friend['id']}/inbox"
                try:
                    remote_server = Node.objects.get(remote_server_url=host_name)
                    req = requests.post(url,
                                        json=post_data,
                                        auth=(remote_server.konnection_username,
                                              remote_server.konnection_password))
                except Node.DoesNotExist:
                    pass

        return post
        
    def perform_create(self, serializer):
        request_author_id = self.request.user.id
        serializer.save(author=Author.objects.get(id=request_author_id))


# api/public/
class PublicPostView(generics.ListAPIView):
    serializer_class = PostSerializer

    # GET: get all public and not unlisted Post
    def get_queryset(self):
        queryset = Post.objects.filter(visibility=Post.PUBLIC, unlisted=False).order_by('-published')
        return queryset
    
    # GET: Paginated posts
    # api/public?page=1&size=2
    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('size') or 50
        page = request.query_params.get('page') or 1
        posts = self.get_queryset() 
        paginator = Paginator(posts, page_size)
        
        data = []
        items = paginator.page(page)
        for item in items:
            data.append(PostSerializer(item).data)

        return Response(data)


# api/author/{AUTHOR_ID}/posts/{POST_ID}/share
class SharePostView(generics.CreateAPIView):
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        sharer_id = request.data.get('from')
        if sharer_id == None:
            return Response({'error':'from is empty!'},
                            status=status.HTTP_400_BAD_REQUEST)
        post_id = self.kwargs['pk']
        post_data = None
        try:
            a_post = Post.objects.get(pk=post_id, unlisted=False)
            post_data = PostSerializer(a_post).data
        except Post.DoesNotExist:
            try:
                sharer_items = Inbox.objects.get(author=sharer_id).items
            except Inbox.DoesNotExist:
                return Response({'error': 'Inbox not found!'},
                                status=status.HTTP_404_NOT_FOUND)
            for item in sharer_items:
                try:
                    item_id = item['id']
                except KeyError:
                    continue
                if post_id in item_id:
                    post_data = item
        if post_data == None:
            return Response({'error': 'Post not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        share_to = request.data.get('share_to')
        if share_to:
            if share_to == 'all':
                friend_list = Following.get_all_local_friends(self, sharer_id)
                remote_friend_list = Following.get_all_remote_friends(self, sharer_id) \
                                     .values()
                if len(friend_list) == 0 and len(remote_friend_list) == 0:
                    return Response({'data': f'No friends to share to'},
                                    status=status.HTTP_200_OK)

                for friend in remote_friend_list:
                    host_name = friend['host']
                    if host_name[-1] == '/':
                        url = f"{friend['host']}api/author/{friend['id']}/inbox/"
                    else:
                        host_name = friend['host'] + '/'
                        url = f"{friend['host']}/api/author/{friend['id']}/inbox/"
                    if "team6" in host_name:
                        url = f"{host_name}author/{friend['id']}/inbox"

                    try:
                        remote_server = Node.objects.get(remote_server_url=host_name)
                        req = requests.post(url,
                                            json=post_data,
                                            auth=(remote_server.konnection_username,
                                                  remote_server.konnection_password))
                    except Node.DoesNotExist:
                        pass

                for friend in friend_list:
                    try:
                        inbox = Inbox.objects.get(author=friend.id)
                        inbox.send_to_inbox(post_data)
                    except:
                        pass
                return Response({'data': f'Shared Post {post_id} with {share_to}'},
                                status=status.HTTP_200_OK)
            else:
                try:
                    Inbox.objects.get(author=share_to).send_to_inbox(post_data)
                except Inbox.DoesNotExist:
                    remote_friend_list = Following.get_all_remote_friends(self, sharer_id)
                    friend = remote_friend_list.get(share_to)

                    if friend:
                        host_name = friend['host']
                        if host_name[-1] == '/':
                            url = f"{friend['host']}api/author/{friend['id']}/inbox/"
                        else:
                            host_name = friend['host'] + '/'
                            url = f"{friend['host']}/api/author/{friend['id']}/inbox/"
                        if "team6" in host_name:
                            url = f"{host_name}author/{friend['id']}/inbox"
                        try:
                            remote_server = Node.objects.get(remote_server_url=host_name)
                        except Node.DoesNotExist:
                            return Response({'data': 'Node not found!'},
                                            status=status.HTTP_400_BAD_REQUEST)

                        req = requests.post(url,
                                            json=post_data,
                                            auth=(remote_server.konnection_username,
                                                  remote_server.konnection_password))
                        return Response({'data': f'Shared Post {post_id} with Author '
                                                 f'{share_to} on {host_name}.'},
                                        status=req.status_code)
                    else:
                        return Response({'error': 'Friend not found!'},
                                        status=status.HTTP_404_NOT_FOUND)
                return Response({'data': f'Shared Post {post_id} with Author {share_to}.'},
                                status=status.HTTP_200_OK)
        else:
            return Response({'error':'share_to is empty!'},
                            status=status.HTTP_400_BAD_REQUEST)
