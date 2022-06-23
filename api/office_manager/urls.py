from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.office_manager.views.product import ProductModelViewSet

router = DefaultRouter()
router.register('product', ProductModelViewSet)
urlpatterns = [
    path('', include(router.urls))
]
