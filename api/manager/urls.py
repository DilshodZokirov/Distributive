from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.manager.views.order import ManagerModelOrderViewSet
from api.manager.views.worker import ManagerWorkerModelApiViewSet

router = DefaultRouter()
router.register('worker', ManagerWorkerModelApiViewSet)
router.register("order", ManagerModelOrderViewSet)
urlpatterns = [
    path('', include(router.urls))
]
