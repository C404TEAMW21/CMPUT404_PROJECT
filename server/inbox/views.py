from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError

from rest_framework import authentication, generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from posts.serializers import PostSerializer
from author.serializers import AuthorProfileSerializer
from main.models import Author
from nodes.models import Node
from main import utils
from posts.models import Post
from likes.models import Like
from .models import Inbox
from .serializers import InboxSerializer
from urllib.parse import urlparse
import requests
import json
import uuid


# api/author/{AUTHOR_ID}/inbox/
class InboxView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InboxSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def get_inbox(self):
        request_author_id = uuid.UUId(self.kwargs['author_id'])

        if self.request.user.id != request_author_id:
            raise PermissionDenied(
                detail={'error': ['You do not have permission to this inbox.']})

        if not self.request.user.adminApproval:
            raise PermissionDenied(
                detail={'error': ['User has not been approved by admin.']})

        return get_object_or_404(Inbox, author=Author.objects
                                 .get(id=self.request.user.id))

    # GET: get Inbox of an user
    def get(self, request, *args, **kwargs):
        inbox = self.get_inbox()
        serializer = InboxSerializer(inbox, context={'request': request})
        return Response(serializer.data)

    # POST: send a Post, Like or Follow to Inbox
    def post(self, request, *args, **kwargs):
        request_author_id = uuid.UUID(self.kwargs['author_id'])
        inbox_type = request.data.get('type')
        if inbox_type is not None: inbox_type = inbox_type.lower() 
        host_name = request.get_host()

        if inbox_type == 'post':
            post_id = request.data.get('id')
            try:
                Inbox.objects.get(author=request_author_id).send_to_inbox(request.data)
            except Inbox.DoesNotExist as e:
                return Response({'error':'Author not found! Please check author_id in URL.'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({'data':f'Shared Post {post_id} with Author '
                                    f'{request_author_id} on {host_name}.'},
                            status=status.HTTP_200_OK)
        elif inbox_type == 'like':
            id_url = request.data.get('object')
            parsed_uri = urlparse(id_url)
            object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

            # Sending a LIKE from (us or remote server) to us
            if (object_host == utils.HOST):
                try:
                    Inbox.objects.get(author=request_author_id).send_to_inbox(request.data)
                except Inbox.DoesNotExist as e:
                    return Response({'error':'Author not found! Please check author_id in URL.'},
                                    status=status.HTTP_404_NOT_FOUND)
            # Sending a LIKE from us to remote server
            else:
                try:
                    remote_server = Node.objects.get(remote_server_url=object_host)
                except Node.DoesNotExist:
                    return Response({'error':'Could not find remote server user'}, status=status.HTTP_404_NOT_FOUND)

                if 'team6' in object_host:
                    request_author_id = request_author_id.hex
                    request_url = f"{object_host}author/{request_author_id}/inbox"
                else:
                    request_url = f"{object_host}api/author/{request_author_id}/inbox/"

                r = requests.post(
                    request_url,
                    json=request.data,
                    auth=('team12hailan', 'konnections')
                )

                if r.status_code < 200 or r.status_code >= 300:
                    return Response({'error':'Could not complete the request to the remote server'},
                        status=r.status_code)
            
            # Gather information for the Like object creation
            try:
                object_type = Like.LIKE_COMMENT if ('comments' in id_url) else Like.LIKE_POST
                if (id_url.endswith('/')):
                    object_id = id_url.split('/')[-2]
                else:
                    object_id = id_url.split('/')[-1]
                like_author_id = request.data.get('author')['id'].split('/')[-1]
                Like.objects.create(
                    author=request.data.get('author'), author_id=like_author_id, 
                    object=id_url, object_type=object_type, object_id=object_id
                )
            except IntegrityError:
                return Response({'data':f'You have already sent a like to {object_type} {id_url} on {host_name}.'},
                            status=status.HTTP_200_OK)
            
            return Response({'data':f'Sent like to {object_type} {id_url} on {host_name}.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid type, only \'post\', \'like\''},
                            status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Clear the inbox
    def delete(self, request, *args, **kwargs):
        inbox = self.get_inbox()
        length = len(inbox.items)
        inbox.items.clear()
        inbox.save()
        return Response({'data':f'Deleted {length} messages.'}, status=status.HTTP_200_OK)
