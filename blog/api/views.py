from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject

from blog.models import Post, Tag
from blango_auth.models import User
from blog.api.serializers import (
  PostSerializer,
  UserSerializer,
  PostDetailSerializer,
  TagSerializer
)


class PostViewSet(viewsets.ModelViewSet):
  permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
  queryset = Post.objects.all()

  def get_serializer_class(self):
    if self.action in ("list", "create"):
      return PostSerializer
    return PostDetailSerializer


class UserDetailView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_field = 'email'


class TagViewSet(viewsets.ModelViewSet):
  serializer_class = TagSerializer
  queryset = Tag.objects.all()

  @action(methods=["get"], detail=True, name="Posts with the Tag")
  def posts(self, request, pk=None):
    tag = self.get_object()
    post_serializer = PostSerializer(
        tag.posts, many=True, context={"request": request}
    )
    return Response(post_serializer.data)