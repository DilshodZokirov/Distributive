from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.agent.serializers.product import ProductAllCategorySerializer
from apps.product.models import Product


class AgentProductModelApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Product.objects.all().order_by('-id')
    filter_backends = (SearchFilter,)
    serializer_class = ProductAllCategorySerializer
