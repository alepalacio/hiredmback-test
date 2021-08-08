from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
#from users.views import Login

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    # path("account/", include("rest_email_auth.urls")),
    path("profiles/", include("profile.urls")),
    #path("", Login.as_view(), name="login")
    path("rest-auth/", include('rest_auth.urls')),
    #path("rest-auth/registration/", include('rest_auth.registration.urls')),
]
