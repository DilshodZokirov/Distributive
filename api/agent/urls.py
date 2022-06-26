from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.agent.views.worker import WorkerModelApiViewSet

router = DefaultRouter()
# router.register('product', ProductModelViewSet)
router.register('worker', WorkerModelApiViewSet)
# router.register('order', OrderModelViewSet)
urlpatterns = [
    path('', include(router.urls))
]
