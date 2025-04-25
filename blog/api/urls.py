from django.urls import path, include
from rest_framework.authtoken import views as token_views

from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import PostListCreateView, PostRetieveUpdateDeleteView

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="api_post_list"),
    path("posts/<int:pk>", PostRetieveUpdateDeleteView.as_view(), name="api_post_detail"),
    path("auth/", include("rest_framework.urls")),
    path('get-token/', token_views.obtain_auth_token, name='get_token')
]

urlpatterns = format_suffix_patterns(urlpatterns)