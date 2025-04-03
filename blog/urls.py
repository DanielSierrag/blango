from django.urls import path
import blog.views

urlpatterns = [
    # other patterns
    path("", blog.views.index),
]