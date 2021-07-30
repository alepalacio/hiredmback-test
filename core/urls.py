from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("rest_email_auth.urls")),
    path("account/", include("users.urls")),
    path("", include("profile.urls")),
    path('rest-auth/', include('rest_auth.urls')),
    #path('rest-auth/registration/', include('rest_auth.registration.urls'))
    #path("account/", include("rest_auth.urls")),
]
