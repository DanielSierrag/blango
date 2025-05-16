from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.db.models import Q
from django.utils import timezone
from django.http import Http404

from datetime import timedelta

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

  def get_queryset(self):
    if self.request.user.is_anonymous:
      # Just published posts
      queryset = self.queryset.filter(published_at__lte=timezone.now())
    elif self.request.user.is_staff:
      # Allow all
      queryset = self.queryset
    else:
      queryset = self.queryset.filter(
        # Owned posts or just published posts
        Q(published_at__lte=timezone.now() | Q(author=self.request.user))
      )

    time_period_name = self.kwargs.get('period_name')

    if not time_period_name:
      return queryset
    
    if time_period_name == "new":
        return queryset.filter(
            published_at__gte=timezone.now() - timedelta(hours=1)
        )
    elif time_period_name == "today":
        return queryset.filter(
            published_at__date=timezone.now().date(),
        )
    elif time_period_name == "week":
        return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
    else:
        raise Http404(
            f"Time period {time_period_name} is not valid, should be "
            f"'new', 'today' or 'week'"
        )

  @method_decorator(cache_page(120))
  @method_decorator(vary_on_headers('Authorization', 'Cookie'))
  def list(self, *args, **kwargs):
    return super(PostViewSet, self).list(*args, **kwargs)

  def get_serializer_class(self):
    if self.action in ("list", "create"):
      return PostSerializer
    return PostDetailSerializer

  @method_decorator(cache_page(300))
  @method_decorator(vary_on_headers('Authorization'))
  @method_decorator(vary_on_cookie)
  @action(methods=['get'], detail=False, name='Post by the logged in user')
  def mine(self, request):
    if not request.user.is_authenticated:
      raise PermissionDenied('You must be logged in to se which Posts are yours')
    posts = self.get_queryset().filter(author=request.user)
    serialzer = self.get_serializer_class()(many=True, context={'request': request})
    return Response(serialzer.data)


class UserDetailView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_field = 'email'

  @method_decorator(cache_page(300))
  def get(self, *args, **kwargs):
    return super(UserDetailView, self).get(*args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
  serializer_class = TagSerializer
  queryset = Tag.objects.all()

  @method_decorator(cache_page(300))
  def list(self, *args, **kwargs):
    return super(TagViewSet, self).list(*args, **kwargs)

  @method_decorator(cache_page(300))
  def retrieve(self, *args, **kwargs):
    return super(TagViewSet, self).retrieve(*args, **kwargs)

  @action(methods=["get"], detail=True, name="Posts with the Tag")
  def posts(self, request, pk=None):
    tag = self.get_object()
    post_serializer = PostSerializer(
        tag.posts, many=True, context={"request": request}
    )
    return Response(post_serializer.data)