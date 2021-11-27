from django.urls import path
from rest_framework.routers import SimpleRouter

from accounts.views import CreateUserView, LoginUserView

router = SimpleRouter()
router.register("accounts", CreateUserView)

urlpatterns = [
    path("login/", LoginUserView.as_view()),
]

urlpatterns += router.urls
