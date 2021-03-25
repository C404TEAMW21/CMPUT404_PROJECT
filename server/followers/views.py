from django.db.models import query
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


#<slug:id>/followers/
class FollowersView(generics.RetrieveAPIView):
    serializer_class = FollowersSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        self.request_author_id = self.kwargs['id']

        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})

        try: 
            author_followers_exists = models.Followers.objects.filter(author=self.request_author_id).exists()
            author_following_exists = models.Following.objects.filter(author=self.request_author_id).exists()
            if not author_followers_exists:
                authorObj = models.Author.objects.get(id=self.request_author_id)
                models.Followers.objects.create(author=authorObj)
            if not author_following_exists:
                authorObj = models.Author.objects.get(id=self.request_author_id)
                models.Following.objects.create(author=authorObj)
        except:
            raise ValidationError({"error": ["Author not found"]})

        try:
            return models.Followers.objects.get(author=self.request_author_id)
        except:
            raise ValidationError({"error": ["Author not found"]})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        remote_followers_list = models.Followers.get_all_remote_followers(self, self.kwargs['id'])

        for item in serializer.data['followers']:
            remote_followers_list.append(item)

        return Response({
            'type': 'followers',
            'items': remote_followers_list,
        })

#/<slug:id>/followers/<slug:foreignId>/
class FollowersModificationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FollowersModificationSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        self.request_author_id = self.kwargs['id']
        self.request_foreign_author_id = self.kwargs['foreignId']
        
        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})

        try: 
            author_followers_exists = models.Followers.objects.filter(author=self.request_author_id).exists()
            author_following_exists = models.Following.objects.filter(author=self.request_author_id).exists()
            foreign_author_followers_exists = models.Followers.objects.filter(author=self.request_foreign_author_id).exists()
            foreign_author_following_exists = models.Following.objects.filter(author=self.request_foreign_author_id).exists()
            if not author_followers_exists:
                authorObj = models.Author.objects.get(id=self.request_author_id)
                models.Followers.objects.create(author=authorObj)
            if not author_following_exists:
                authorObj = models.Author.objects.get(id=self.request_author_id)
                models.Following.objects.create(author=authorObj)
            if not foreign_author_followers_exists:
                authorObj = models.Author.objects.get(id=self.request_foreign_author_id)
                models.Followers.objects.create(author=authorObj)
            if not foreign_author_following_exists:
                authorObj = models.Author.objects.get(id=self.request_foreign_author_id)
                models.Following.objects.create(author=authorObj)
        except:
            raise ValidationError({"error": ["Author not found"]})


        try:
            self.author = models.Author.objects.get(id=self.request_author_id)
            self.foreignAuthor = models.Author.objects.get(id=self.request_foreign_author_id)
                  
            return models.Followers.objects.filter(author=self.request_author_id)

        except:
            raise ValidationError({"error": ["User not found"]})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
                
        return Response({
            'type': 'follower',
            'items': [{
                'status': self.foreignAuthor in serializer.data['followers'],
                'author':  self.author.id,
                'follower': self.foreignAuthor.id,
            }]
        })

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.get_serializer(instance, data=request.data, partial=True)


        if (self.request_author_id == self.request_foreign_author_id):
            return Response({
                'error': ['You cannot follow yourself']}, status=status.HTTP_400_BAD_REQUEST)
        elif (not self.request.user.adminApproval):
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
        
        # Test required fields 
        try:
            actorObj = request.data['actor']
            actorHost = request.data['actor']['host']
            objectHost = request.data['object']['host']
            actorId = request.data['actor']['id']
        except:
            return Response({
                'error': ['Please provide required fields']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle all cases 
        inboxData = {}
        if objectHost == utils.HOST and actorHost != utils.HOST:
            authorObj = models.Author.objects.get(id=self.request_author_id)
            author = models.Followers.objects.get(author=authorObj)

            if actorHost not in author.remoteFollowers:
                author.remoteFollowers[actorHost] = {}

            author.remoteFollowers[actorHost][actorId] = actorObj
            author.save()

            inboxData = request.data
        elif objectHost and actorHost == utils.HOST:
            
            if (str(self.request_foreign_author_id) != str(request.user.id)):
                return Response({
                    'error': ['This is not your account, you cannot follow this author']}, status=status.HTTP_403_FORBIDDEN) 
            
            author_obj = models.Author.objects.get(id=self.request_author_id)
            author = models.Followers.objects.get(author=author_obj)
            foreign_author_obj = models.Author.objects.get(id=self.request_foreign_author_id)
            foreign_author = models.Following.objects.get(author=foreign_author_obj)

            foreign_author.following.add(author_obj)
            author.followers.add(foreign_author_obj)
            author.save()

            inboxData['type'] = 'follow'
            inboxData['summary'] = f"{self.foreignAuthor.username} wants to follow {self.author.username}"
            inboxData['actor'] = AuthorProfileSerializer(foreign_author_obj).data
            inboxData['object'] = AuthorProfileSerializer(author).data
            
        elif objectHost != utils.HOST and actorHost == utils.HOST:
            # TODO: Connect with other team
            a = ''
        else: 
            return Response({
                'error': ['Bad request']}, status=status.HTTP_400_BAD_REQUEST)


        authorObj = models.Author.objects.get(id=self.request_author_id)
        inbox = Inbox.objects.get(author=authorObj)
        inbox.items.append(inboxData)
        inbox.save()
        
        return Response({
            'type': 'follow',
            'items': [{
                'status': True,
                'author':  self.author.id,
                'follower': self.foreignAuthor.id,
            }]
        })
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            raise ValidationError({"error": ["User not found"]})

        if (str(self.request_foreign_author_id) != str(request.user.id)):
           return Response({
                'error': ['This is not your account, you cannot unfollow this author']}, status=status.HTTP_403_FORBIDDEN) 
        elif (self.request_author_id == self.request_foreign_author_id):
            return Response({
                'error': ['You cannot unfollow yourself']}, status=status.HTTP_400_BAD_REQUEST)
        elif (self.foreignAuthor not in serializer.data['followers']):
            return Response({
                'error': ['You are not following this author, hence, you can unfollow']}, status=status.HTTP_400_BAD_REQUEST)
        elif (not self.request.user.adminApproval):
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})


        authorObj = models.Author.objects.get(id=self.request_author_id)
        author = models.Followers.objects.get(author=authorObj)
        foreignAuthor = models.Author.objects.get(id=self.request_foreign_author_id)

        author.followers.remove(foreignAuthor)
        author.save()

        FriendRequest.objects.filter(follower=foreignAuthor, author=authorObj).delete()

        return Response({
            'type': 'unfollow',
            'items': [{
                'status': False,
                'author':  author.author.id,
                'follower': foreignAuthor.id,
            }]
        })

class FollowersFriendView(generics.RetrieveAPIView):
    serializer_class = AuthorProfileSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        author_id = self.kwargs['id']
       
        try:
            return models.Following.get_all_local_friends(self, author_id)
        except:
           return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        remote_following_list = models.Following.get_all_remote_friends(self, self.kwargs['id'])

        for item in AuthorProfileSerializer(instance, many=True).data:
            remote_following_list.append(item)
            
        return Response(remote_following_list)
