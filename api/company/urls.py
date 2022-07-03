from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.delivery.views.worker import DeliveryWorkerModelApiViewSet
from api.company.views.company import CompanyModelViewSet

router = DefaultRouter()
router.register('company', CompanyModelViewSet)
urlpatterns = [
    path('', include(router.urls))
]
