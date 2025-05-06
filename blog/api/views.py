from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject

from blog.models import Post
from blango_auth.models import User
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer


class PostListCreateView(generics.ListCreateAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticatedOrReadOnly]
  queryset = Post.objects.all()
  serializer_class = PostSerializer


class PostRetieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
  queryset = Post.objects.all()
  serializer_class = PostDetailSerializer

class UserDetailView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_field = 'email'