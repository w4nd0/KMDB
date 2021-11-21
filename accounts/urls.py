from django.urls import path

from accounts.views import CreateUserView, LoginUserView

urlpatterns = [
    path("accounts/", CreateUserView.as_view()),
    path("login/", LoginUserView.as_view()),
]
