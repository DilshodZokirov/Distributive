from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LoginUserModelView, RegisterUserApiView

router = DefaultRouter()
router.register("login", LoginUserModelView)
urlpatterns = [
    path("", include(router.urls)),
    # path('login/', LoginUserAPIView.as_view()),
    path("registration/", RegisterUserApiView.as_view())
]
