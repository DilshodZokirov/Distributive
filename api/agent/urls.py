from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.agent.views.product import AgentProductModelApiViewSet
from api.agent.views.worker import WorkerModelApiViewSet

router = DefaultRouter()
router.register('worker', WorkerModelApiViewSet)
router.register('product', AgentProductModelApiViewSet)
urlpatterns = [
    path('', include(router.urls))
]
