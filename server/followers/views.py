from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import generics, permissions, status

from main import models, utils
from .models import FriendRequest
from inbox.models import Inbox
from followers.serializers import FollowersSerializer, FollowersModificationSerializer
from author.serializers import AuthorProfileSerializer

from nodes.models import Node
import requests 
from urllib.parse import urlparse
import json
import re

def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'https://{}'.format(url)
    return url

def admin_approval_safeguard(self):
    if not self.request.user.adminApproval:
        raise AuthenticationFailed(
            detail={"error": ["User has not been approved by admin"]})

TEAM6_HOST = "https://team6-project-socialdistrib.herokuapp.com/"
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

# <slug:id>/following/<slug:foreignId>/
class FollowingView(generics.RetrieveAPIView):
    serializer_class = FollowersSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        admin_approval_safeguard(self)
        request_author_id = self.kwargs['id']
        request_foreign_author_id = self.kwargs['foreignId']
        try:
            author_following = models.Following.objects.get(
                author=request_author_id)
        except:
            return Response(
                {'error': ["Author not found"]},
                status=status.HTTP_404_NOT_FOUND)
        
         # Check required fields in the body
        try:
            actor_host = request.data['actor']['host']
            object_host = request.data['object']['host']
        except:
            return Response({
                'error': ['Please provide required fields']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Remote following
            if actor_host == utils.HOST and object_host != utils.HOST:
                remote_following_ids = author_following.remote_following.keys()
                if request_foreign_author_id in remote_following_ids:
                    return Response({
                        'type': 'following',
                        'items': [{
                            'status': True,
                            'author':  request_author_id,
                            'following': request_foreign_author_id,
                        }]
                    })
            # Local following
            elif actor_host == utils.HOST and object_host == utils.HOST:
                try:
                    author = models.Author.objects.get(id=request_foreign_author_id)
                except:
                    Response(
                        {'error': ["Following Author doesn't exist"]},
                        status=status.HTTP_400_BAD_REQUEST)

                local_following = author_following.following.all()
                local_following_json = AuthorProfileSerializer(local_following, many=True).data
                for i in local_following_json:
                    if(i.get('id') == request_foreign_author_id):
                        return Response({
                            'type': 'following',
                            'items': [{
                                'status': True,
                                'author':  request_author_id,
                                'following': request_foreign_author_id,
                            }]
                        })

            return Response({
                'type': 'following',
                'items': [{
                    'status': False,
                    'author':  request_author_id,
                    'following': request_foreign_author_id,
                }]
            })
        except:
            return Response(
                {'error': ["Bad Request"]},
                status=status.HTTP_400_BAD_REQUEST)

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
            object_data = request.data['object']
            object_id = request.data['object']['id']
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
            actor_data["id"] = request_foreign_author_id
            author.remoteFollowers[request_foreign_author_id] = actor_data

            author.save()

            inboxData = request.data
        # Local Follower
        elif object_host == utils.HOST and actor_host == utils.HOST:
            if str(request_foreign_author_id) != str(request.user.id):
                return Response({
                    'error': ['This is not your account, you cannot follow this author']}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                foreign_author_obj = models.Author.objects.get(
                    id=request_foreign_author_id)
                foreign_author_following = models.Following.objects.get(author=foreign_author_obj)
                author_obj = models.Author.objects.get(id=request_author_id)
                author_follower = models.Followers.objects.get(author=author_obj)
            except:
                return Response(
                    {'error': ["Author not found"]},
                        status=status.HTTP_404_NOT_FOUND)

            author_follower.followers.add(foreign_author_obj)
            author_follower.save()
            foreign_author_following.following.add(author_obj)
            foreign_author_following.save()

            inboxData['type'] = 'follow'
            inboxData['summary'] = f"{foreign_author_obj.username} wants to follow {author_obj.username}"
            inboxData['actor'] = AuthorProfileSerializer(foreign_author_obj).data
            inboxData['object'] = AuthorProfileSerializer(author_follower).data
        # us following remote author
        elif object_host != utils.HOST and actor_host == utils.HOST:
            # For Team 6
            if object_host == TEAM6_HOST:
                correct_url = formaturl(object_host)
                parsed_uri = urlparse(correct_url)
                object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                print(object_host)
                try:
                    node = Node.objects.get(remote_server_url=object_host)
                
                    response = requests.put(f"{object_host}author/{request_author_id}/followers/{request_foreign_author_id}", json=request.data, auth=(node.konnection_username, node.konnection_password))
                 
                    if response.status_code != 201:
                        # Their problem
                        return Response({'error': ['Contact team 6 for the error']}, status=response.status_code)
                    else:
                        author = models.Following.objects.get(author=request_foreign_author_id)
                        object_data["id"] = request_author_id
                     
                        author.remote_following[request_author_id] = object_data

                        author.save()
   
                        return Response({'message': ['Successful']}, status=response.status_code)
                except Exception:
                    # Our problem
                    return Response({'error': ["Bad request"]}, status=status.HTTP_400_BAD_REQUEST)
                

            parsed_uri = urlparse(object_host)
            object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            
            try:
                node = Node.objects.get(remote_server_url=object_host)
                response = requests.put(f"{object_host}api/author/{request_author_id}/followers/{request_foreign_author_id}/", json=request.data, auth=(node.konnection_username, node.konnection_password))

                if response.status_code != 201:
                    # Their problem
                    return Response({'error': ['Following unsuccessful']}, status=response.status_code)
                else:
                    author = models.Following.objects.get(author=request_foreign_author_id)
                    author.remote_following[object_id] = object_data
                    author.save()

                    return Response({'message': ['Successful']}, status=response.status_code)
            except Exception:
                # Our problem
                return Response({'error': ["Bad request"]}, status=status.HTTP_400_BAD_REQUEST)
           

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

        # Check required fields in the body
        try:
            host = request.data['host']
        except:
            return Response({
                'error': ['Please provide required fields']}, status=status.HTTP_400_BAD_REQUEST)

        # Local remove local following
        if host == utils.HOST: 
            try: 
                author_obj = models.Author.objects.get(id=request_author_id)
                author_followers = models.Followers.objects.get(author=author_obj)
                foreign_author_obj = models.Author.objects.get(id=request_foreign_author_id)
                foreign_author_following = models.Following.objects.get(author=foreign_author_obj)

                author_followers.followers.remove(foreign_author_obj)
                author_followers.save()
                foreign_author_following.following.remove(author_obj)
                foreign_author_following.save()
            except:
                try:
                    author_obj = models.Author.objects.get(id=request_author_id)
                    author = models.Followers.objects.get(author=author_obj)
                    author.remoteFollowers.pop(request_foreign_author_id)
                    author.save()
                except:
                    return Response({
                        'error': ['Bad request- user not found']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            
            # Local remove remote following
            try:
                # For Team 6
                if host == TEAM6_HOST:
                    correct_url = formaturl(host)
                    parsed_uri = urlparse(correct_url)
                    object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

                    try:
                        node = Node.objects.get(remote_server_url=object_host)
                    
                        response = requests.delete(f"{object_host}author/{request_author_id}/followers/{request_foreign_author_id}", auth=(node.konnection_username, node.konnection_password))
                    
                        if response.status_code != 200:
                            # Their problem
                            return Response({'error': ['Contact team 6 for the error']}, status=response.status_code)
                        else:
                            foreign_author_obj = models.Author.objects.get(id=request_foreign_author_id)
                            foreign_author_following = models.Following.objects.get(author=foreign_author_obj)
                            foreign_author_following.remote_following.pop(request_author_id)
                            foreign_author_following.save()
    
                            return Response({'message': ['Successful']}, status=response.status_code)
                    except Exception:
                        # Our problem
                        return Response({'error': ["Bad request"]}, status=status.HTTP_400_BAD_REQUEST)

                parsed_uri = urlparse(host)
                object_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                
   
                node = Node.objects.get(remote_server_url=object_host)
                response = requests.delete(f"{object_host}api/author/{request_author_id}/followers/{request_foreign_author_id}/", auth=(node.konnection_username, node.konnection_password))

                if response.status_code != 204:
                    # Their problem
                    return Response({'error': ['unfollowing unsuccessful - others sever issue']}, status=response.status_code)
                else:
                    # Remote remove following of local
                    foreign_author_obj = models.Author.objects.get(id=request_foreign_author_id)
                    foreign_author_following = models.Following.objects.get(author=foreign_author_obj)
                    foreign_author_following.remote_following.pop(request_author_id)
                    foreign_author_following.save()
            except:
                return Response({'error': ["Bad request"]}, status=status.HTTP_400_BAD_REQUEST)
            

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
