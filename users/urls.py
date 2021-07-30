from django.urls import path
from . import views


urlpatterns = [
    path("", views.AccountUrlList.as_view(), name="api-overview"),
    # path("log-in", views.APILoginView.as_view(), name="api-login"),
]
