from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.agent.serializers.product import ProductAllCategorySerializer, CategoryAllSerializer, CategoryGetOneSerializer, \
    ProductOneSerializer
from apps.product.models import Product, Category
from apps.user.models import Company


class AgentProductModelApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Product.objects.all().order_by('-id')
    filter_backends = (SearchFilter,)
    serializer_class = ProductAllCategorySerializer

    @action(methods=['get'], detail=False)
    def category_all(self, request):
        company_id = request.user.company_id
        category = Category.objects.filter(company_id=company_id)
        serializer = CategoryAllSerializer(category, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def category_one(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        serializer = CategoryGetOneSerializer(category)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def product_one(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        serializer = ProductOneSerializer(product)
        return Response(serializer.data)
    # def retrieve(self, request, *args, **kwargs):
    #     return super(AgentProductModelApiViewSet, self).retrieve(self, request, *args, **kwargs)
