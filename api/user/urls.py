from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LoginUserModelView

router = DefaultRouter()
router.register("authorization", LoginUserModelView)
urlpatterns = [
    path("", include(router.urls)),
]
