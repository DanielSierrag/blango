from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # other patterns
    path("", views.index),
    path("post/<slug>", views.post_detail, name='post_detail')
]