from django.urls import path, include, re_path
from rest_framework.authtoken import views as token_views
from rest_framework.routers import SimpleRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import os

from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import (
  PostViewSet,
  UserDetailView,
  TagViewSet
)

router = SimpleRouter()
router.register("posts", PostViewSet)
router.register("tags", TagViewSet)

# Posts URLs
urlpatterns = [
    path("users/<str:email>", UserDetailView.as_view(), name='api_user_detail'),
    path("auth/", include("rest_framework.urls")),
    path('get-token/', token_views.obtain_auth_token, name='get_token')
]

# Post & Tags URLs
urlpatterns += router.urls

urlpatterns += [path(
  'posts/by-time/<str:period_name>/',
  PostViewSet.as_view({'get': 'list'}),
  name='posts_by_time'
)]

# Documentation urls
schema_view = get_schema_view(
  openapi.Info(
    title='Blango API',
    default_version='v1',
    description='API for blango blog',
  ),
  url=f"https://{os.environ.get('CODIO_HOSTNAME')}-8000.codio.io/api/v1",
  public=True,
)

urlpatterns += [
  # .json or .yaml format (No UI endpoint)
  re_path(
    r"^swagger(?P<file_format>\.json|\.yaml)$",
    schema_view.without_ui(cache_timeout=0),
    name='schema-json'
  ),
  # swagger interactive documentation
  path(
    'swagger/',
    schema_view.with_ui("swagger", cache_timeout=0),
    name='schema-swagger-ui'
  ),
]

urlpatterns = format_suffix_patterns(urlpatterns)