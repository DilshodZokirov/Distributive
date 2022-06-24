from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.office_manager.serializers.add_member import UserCreateSerializer
from api.office_manager.views.add_member import AddUserModelViewSet
from api.office_manager.views.order import OrderModelViewSet
from api.office_manager.views.product import ProductModelViewSet

router = DefaultRouter()
router.register('product', ProductModelViewSet)
router.register('add_member', AddUserModelViewSet)
router.register('order', OrderModelViewSet)
urlpatterns = [
    path('', include(router.urls))
]
