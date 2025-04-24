from rest_framework import generics

from blog.models import Post
from blog.api.serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer


class PostRetieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer