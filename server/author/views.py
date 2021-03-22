from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from author.serializers import AuthorSerializer, AuthAuthorSerializer, AuthorProfileSerializer

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

class AllAuthorsView(generics.ListAPIView):
    """Get all authors in the system"""
    serializer_class = AuthorProfileSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
        
        return get_user_model().objects.filter(type='author', adminApproval=True)
