from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import urljoin
import requests

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from author.serializers import AuthorSerializer, AuthAuthorSerializer, AuthorProfileSerializer
from nodes.models import Node

class CreateAuthorView(generics.CreateAPIView):
    """Create a new author in the system"""
    serializer_class = AuthorSerializer

class AuthAuthorView(ObtainAuthToken):
    """Authenticate author in the system"""
    serializer_class = AuthAuthorSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        author = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=author)

        if not author.adminApproval:
            return Response({"error": ["User has not been approved by admin"]}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'token': token.key,
        })

class AuthorProfileView(generics.RetrieveUpdateAPIView):
    """Get author in the system"""
    serializer_class = AuthorProfileSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "put"]

    def get_object(self):
        id = self.kwargs['pk']
        try:
            return get_object_or_404(get_user_model().objects, id=id)
        except:
            raise ValidationError({"error": ["User not found"]})

class MyProfileView(generics.RetrieveAPIView):
    """Get authenticated author profile in the system"""
    serializer_class = AuthorProfileSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get"]

    def get_object(self):
        if not self.request.user.adminApproval:
            raise AuthenticationFailed(detail ={"error": ["User has not been approved by admin"]})
            
        return self.request.user

class AllLocalAuthorsView(generics.ListAPIView):
    """Get all local authors in the system"""
    serializer_class = AuthorProfileSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
        
        return get_user_model().objects.filter(type='author', adminApproval=True)

class AllAuthorsView(generics.ListAPIView):
    """Get all authors including remote authors in the system"""
    serializer_class = AuthorProfileSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
        all_authors = []
        local = list(get_user_model().objects.filter(type='author', adminApproval=True))
        all_authors.extend(local)

        for remote_server in Node.objects.all():
            if "team6" in remote_server.remote_server_url:
                url = urljoin(remote_server.remote_server_url, "authors")
            else:
                url = urljoin(remote_server.remote_server_url, "api/authors/")

            req = requests.get(url,
                               auth=(remote_server.konnection_username,
                                     remote_server.konnection_password))
            remote_authors = req.json()
            all_authors.extend(remote_authors)

        return all_authors
