from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import PostListCreateView, PostRetieveUpdateDeleteView

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="api_post_list"),
    path("posts/<int:pk>", PostRetieveUpdateDeleteView.as_view(), name="api_post_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)