from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.delivery.views.worker import DeliveryWorkerModelApiViewSet

router = DefaultRouter()
router.register('worker', DeliveryWorkerModelApiViewSet)
urlpatterns = [
    path('', include(router.urls))
]
