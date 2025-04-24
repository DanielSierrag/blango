"""blango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from blango_auth import views as ba_views
import debug_toolbar
import blog

from django_registration.backends.activation.views import RegistrationView
from blango_auth.forms import BlangoRegistrationForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
    "accounts/register/",
    RegistrationView.as_view(form_class=BlangoRegistrationForm),
    name="django_registration_register",
    ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include('allauth.urls')),
    path('accounts/profile/', ba_views.profile, name='profile'),
    path('blog/', include('blog.urls')),
    path('api/v1/', include('blog.api.urls')),
    path('ip/', blog.views.get_ip)
]

if settings.DEBUG:
  urlpatterns += [
    path("__debug__/", include(debug_toolbar.urls))
  ]
