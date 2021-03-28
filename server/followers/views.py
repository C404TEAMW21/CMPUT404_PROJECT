from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import generics, permissions, status

from main import models, utils
from .models import FriendRequest
from inbox.models import Inbox
from followers.serializers import FollowersSerializer, FollowersModificationSerializer
from author.serializers import AuthorProfileSerializer

import requests as HTTPRequests
import json


def admin_approval_safeguard(self):
    if not self.request.user.adminApproval:
        raise AuthenticationFailed(
            detail={"error": ["User has not been approved by admin"]})

# <slug:id>/followers/
class FollowersView(generics.RetrieveAPIView):
    serializer_class = FollowersSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        admin_approval_safeguard(self)
        request_author_id = self.kwargs['id']
        try:
            author_followers = models.Followers.objects.get(
                author=request_author_id)
        except:
            return Response(
                {'error': ["Author not found"]},
                status=status.HTTP_404_NOT_FOUND)

        remote_followers_list = list(
            models.Followers.get_all_remote_followers(self, self.kwargs['id']).values())

        serializer = self.get_serializer(author_followers)

        for item in serializer.data['followers']:
            remote_followers_list.append(item)

        return Response({
            'type': 'followers',
            'items': remote_followers_list,
        })

# /<slug:id>/followers/<slug:foreignId>/


class FollowersModificationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Followers.objects.all()
    serializer_class = FollowersModificationSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        request_author_id = self.kwargs['id']
        request_foreign_author_id = self.kwargs['foreignId']
        admin_approval_safeguard(self)
        try:
            instance = models.Followers.objects.filter(
                author=request_author_id)
        except:
            return Response(
                {'error': ["Author not found"]},
                status=status.HTTP_404_NOT_FOUND)

        try:
            remote_follower = instance.values('remoteFollowers')[0]['remoteFollowers']
            if not instance.filter(followers=request_foreign_author_id) and request_foreign_author_id not in remote_follower:
                return Response({'message': ['They are not following one another']}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                {'error': ["Bad Request"]},
                status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'type': 'follower',
                    'items': [{
                        'author':  request_author_id,
                        'follower': request_foreign_author_id,
                    }]
        })

    def update(self, request, *args, **kwargs):
        request_author_id = self.kwargs['id']
        request_foreign_author_id = self.kwargs['foreignId']

        if (request_author_id == request_foreign_author_id):
            return Response({
                'error': ['You cannot follow yourself']}, status=status.HTTP_400_BAD_REQUEST)
        # TODO: Clean up this code
        elif (not self.request.user.adminApproval):
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})

        # Check required fields in the body
        try:
            actor_data = request.data['actor']
            actor_host = request.data['actor']['host']
            actor_id = request.data['actor']['id']
            object_host = request.data['object']['host']
        except:
            return Response({
                'error': ['Please provide required fields']}, status=status.HTTP_400_BAD_REQUEST)

        # Handle all cases
        inboxData = {}
        # Remote Follower
        if object_host == utils.HOST and actor_host != utils.HOST:
            try:
                author_obj = models.Author.objects.get(id=request_author_id)
            except:
                raise ValidationError({"error": ["Author not found"]})

            author = models.Followers.objects.get(author=author_obj)
            author.remoteFollowers[actor_id] = actor_data
            author.save()

            inboxData = request.data
        # Local Follower
        elif object_host and actor_host == utils.HOST:

            if str(request_foreign_author_id) != str(request.user.id):
                return Response({
                    'error': ['This is not your account, you cannot follow this author']}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                foreign_author = models.Author.objects.get(
                    id=request_foreign_author_id)
                author_obj = models.Author.objects.get(id=request_author_id)
                author = models.Followers.objects.get(author=author_obj)
            except:
                return Response(
                    {'error': ["Author not found"]},
                        status=status.HTTP_404_NOT_FOUND)

            author.followers.add(foreign_author)
            author.save()

            inboxData['type'] = 'follow'
            inboxData['summary'] = f"{foreign_author.username} wants to follow {author_obj.username}"
            inboxData['actor'] = AuthorProfileSerializer(foreign_author).data
            inboxData['object'] = AuthorProfileSerializer(author).data
        # us following remote author
        elif object_host != utils.HOST and actor_host == utils.HOST:
            # TODO: Connect with other team
            headers = {'Content-Type': "application/json",
                       'Accept': "application/json"}
            # data={}
            # data['displayName'] = ""
            # r = HTTPRequests.post('https://team6-project-socialdistrib.herokuapp.com/api/query/displayName', json=data, headers=headers, auth=('team12', 'thisis12group'))
            # print(r.text)
        else:
            return Response({
                'error': ['Bad request']}, status=status.HTTP_400_BAD_REQUEST)

        inbox = Inbox.objects.get(author=author_obj)
        inbox.items.append(inboxData)
        inbox.save()

        return Response({
            'type': 'follow',
            'items': [{
                'status': True,
                'author':  request_author_id,
                'follower': request_foreign_author_id,
            }]
        })

    def delete(self, request, *args, **kwargs):
        request_author_id = self.kwargs['id']
        request_foreign_author_id = self.kwargs['foreignId']
        admin_approval_safeguard(self)
        try:
            actor_host = request.data['actor']['host']
            # TODO: DELETE remote author, making HTTP call
        except:
            pass
        # A/follows/B delete 
        try: 
            author_obj = models.Author.objects.get(id=request_author_id)
            author = models.Followers.objects.get(author=author_obj)
            foreign_author_obj = models.Author.objects.get(
                id=request_foreign_author_id)

            author.followers.remove(foreign_author_obj)
            author.save()
        except:
            try:
                author_obj = models.Author.objects.get(id=request_author_id)
                author = models.Followers.objects.get(author=author_obj)
                author.remoteFollowers.pop(request_foreign_author_id)
                author.save()
            except:
                return Response({
                    'error': ['Bad request']}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'type': 'unfollow',
            'items': [{
                'status': False,
                'author':  request_author_id,
                'follower': request_foreign_author_id,
            }]
        })


class FollowersFriendView(generics.RetrieveAPIView):
    serializer_class = AuthorProfileSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        admin_approval_safeguard(self)
        request_author_id = self.kwargs['id']
        try:
            models.Following.objects.get(author=request_author_id)
        except:
            return Response(
                {'error': ["Author not found"]},
                status=status.HTTP_404_NOT_FOUND)

        local_friends = models.Following.get_all_local_friends(self, request_author_id)
        remote_friends_list = list(models.Following.get_all_remote_friends(self, request_author_id).values())
        local_friends_list = AuthorProfileSerializer(local_friends, many=True).data  
        
        for item in local_friends_list:
            remote_friends_list.append(item)

        return Response({
            'type': 'friends',
            'items': remote_friends_list,
        })
