from profile.views import (
    DetailAchievement,
    DeveloperAPIView,
    DeveloperDetailView,
    DevelopersListAPIViews,
    UserAchievements,
)

from django.urls import include, path

urlpatterns = [
    path("developer/", DevelopersListAPIViews.as_view()),
    path("developer/<int:pk>/", DeveloperAPIView.as_view()),
    path("developer/data/<int:pk>/", DeveloperDetailView.as_view()),
    path("developer/<int:pk>/achievements/", UserAchievements.as_view()),
    path("developer/<int:ck>/achievements/<int:pk>/", DetailAchievement.as_view()),
]
