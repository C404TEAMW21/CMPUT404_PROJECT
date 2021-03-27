from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import generics, permissions, status

from django.shortcuts import render, get_object_or_404

from main import models, utils
from .serializers import FollowerSerializer
from .models import Follower, Following


# /<uuid:author_id>/followers/
class FollowersView(generics.ListAPIView):
    http_method_names = ['get']
    serializer_class = FollowerSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # GET: get all followers of author
    def get_queryset(self):
        queryset = Follower.objects.filter(author=self.kwargs['author_id'])
        return queryset

    def get(self, request, *args, **kwargs):
        followers = self.get_queryset()
        items = FollowerSerializer(followers, many=True).data
        response = {
            'type': 'followers',
            'items': items
        }
        return Response(response)

# <uuid:author_id>/followers/<uuid:follower_id>
class FollowersUpdateView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'delete', 'put']
    serializer_class = FollowerSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # returns a follower object with the matching author_id and follower_id
    # returns 404 otherwise
    def get_follower(self):
        author_id = self.kwargs['author_id']
        follower_id = self.kwargs['follower_id']
        a_post = get_object_or_404(
            Follower,
            author=author_id,
            follower_id=follower_id)
        return a_post
    
    # GET the follower object with the right author_id and follower_id
    def retrieve(self, request, *args, **kwargs):
        follower = self.get_follower()
        return Response(FollowerSerializer(follower).data)

    # DELETE - Only the followee or follower can perform the unfollow
    def delete(self, request, *args, **kwargs):
        if (self.kwargs['author_id'] != self.request.user.id
            and self.kwargs['follower_id'] != self.request.user.id
            and self.request.user.type != 'node'):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if self.get_follower():
            self.get_follower().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # PUT - Add a new follower (only follower can perform the follow)
    def update(self, request, *args, **kwargs):
        mandatory_keys = ['id', 'displayName', 'url', 'github', 'host']
        if all(key in request.data for key in mandatory_keys):
            # Check follower or node is performing the action
            if (self.kwargs['follower_id'] != self.request.user.id
            and self.request.user.type != 'node'):
                return Response(status=status.HTTP_403_FORBIDDEN)

            # check if payload follower id is the same as the one in url
            if (str(self.kwargs['follower_id']) != request.data['id']):
                return Response(
                    {'data': 'follower_id in url does not match id in payload'},
                    status=status.HTTP_403_FORBIDDEN
                )
            try:
                author = models.Author.objects.get(id=self.kwargs['author_id'])
            except models.Author.DoesNotExist:
                return Response(
                    {'data': 'Author you want to follow DNE'},
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                follower = Follower.objects.create(
                    author=author,
                    follower_id=self.kwargs['follower_id'],
                    follower=request.data
                )
                data = FollowerSerializer(follower).data

                following = Following.objects.create(
                    author_id=self.kwargs['follower_id'],
                    following_id=self.kwargs['author_id']
                )
            except:
                data = {'data': 'You are already following this author'}
            
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response(
                    {'data': "need all of the following keys: 'id', 'displayName', 'url', 'github', 'host'"},
                    status=status.HTTP_400_BAD_REQUEST)

# <uuid:author_id>/friends/
class FriendView(generics.ListAPIView):
    http_method_names = ['get']
    serializer_class = FollowerSerializer

    # GET: get all followers of author
    def get_queryset(self):
        queryset = Follower.objects.filter(author=self.kwargs['author_id'])
        return queryset

    def get(self, request, *args, **kwargs):
        followers = self.get_queryset()

        friends = []
        for follower in followers:
            if (Following.objects.filter(
                author_id=self.kwargs['author_id'], following_id=follower.follower_id).exists()):
                friends.append(follower.follower)

        response = {
            'type': 'followers',
            'items': friends
        }
        return Response(response)
