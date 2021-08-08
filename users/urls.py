from django.urls import path
from users.views import UserAPIView, UserDetailAPIView, Login, Logout


urlpatterns = [
    path('users/', UserAPIView.as_view(), name="users"),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name="users-detail"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout")
    #path("", views.AccountUrlList.as_view(), name="api-overview"),
    # path("log-in", views.APILoginView.as_view(), name="api-login"),
]
