from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from rest_framework import authentication, generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from posts.serializers import PostSerializer
from author.serializers import AuthorProfileSerializer
from main.models import Author
from posts.models import Post
from .models import Inbox
from .serializers import InboxSerializer

# service/author/{AUTHOR_ID}/inbox/
class InboxView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InboxSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def get_inbox(self):
        request_author_id = self.kwargs['author_id']

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
        request_author_id = self.kwargs['author_id']
        inbox_type = request.data.get('type')
        host_name = request.get_host()

        # TODO: send Like and Follow
        if inbox_type == 'post':
            post_id = request.data.get('id')
            try:
                Inbox.objects.get(author=request_author_id).send_to_inbox(request.data)
            except Inbox.DoesNotExist as e:
                return Response({'error':'Author not found!'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({'data':f'Shared Post {post_id} with Author '
                                    f'{request_author_id} on {host_name}.'},
                            status=status.HTTP_200_OK)
        elif inbox_type == 'Like':
            post_id = request.data.get('object')
            try:
                Inbox.objects.get(author=request_author_id).send_to_inbox(request.data)
            except Inbox.DoesNotExist as e:
                return Response({'error':'Author not found!'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({'data':f'Sent Like to Post {post_id} on {host_name}.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid type, only \'post\', \'Like\''},
                            status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Clear the inbox
    def delete(self, request, *args, **kwargs):
        inbox = self.get_inbox()
        length = len(inbox.items)
        inbox.items.clear()
        inbox.save()
        return Response({'data':f'Deleted {length} messages.'}, status=status.HTTP_200_OK)
