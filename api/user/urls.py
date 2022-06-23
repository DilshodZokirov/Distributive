from django.urls import path

from .views import LoginUserAPIView, RegisterUserApiView

urlpatterns = [
    path('login/', LoginUserAPIView.as_view()),
    path("registration/", RegisterUserApiView.as_view())
]
