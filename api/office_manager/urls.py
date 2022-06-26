from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.office_manager.serializers.worker import UserCreateSerializer
from api.office_manager.views.worker import WorkerModelViewSet
from api.office_manager.views.order import OrderModelViewSet
from api.office_manager.views.product import ProductModelViewSet

router = DefaultRouter()
router.register('product', ProductModelViewSet)
router.register('worker', WorkerModelViewSet)
router.register('order', OrderModelViewSet)
urlpatterns = [
    path('', include(router.urls))
]
