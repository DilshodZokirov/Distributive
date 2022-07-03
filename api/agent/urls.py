from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.agent.views.product import AgentProductModelApiViewSet
from api.agent.views.worker import WorkerModelApiViewSet
from api.agent.views.order import AgentModelOrderViewSet

router = DefaultRouter()
router.register('worker', WorkerModelApiViewSet)
router.register('product', AgentProductModelApiViewSet)
router.register("order", AgentModelOrderViewSet)
urlpatterns = [
    path('', include(router.urls))
]
