from django.urls import path
from users.views import UserAPIView, UserDetailAPIView, Login, Logout, register


urlpatterns = [
    # User list
    path("", UserAPIView.as_view(), name="users"),
    
    # User detail 
    path("<int:pk>", UserDetailAPIView.as_view(), name="users-detail"),
    
    # Registro de usuario
    path('register/', register, name="register"),
    
    # Login de usuario
    path('login/', Login.as_view(), name="login"),
    
    # Logout de usuario
    path('logout/', Logout.as_view(), name="logout"),
]
