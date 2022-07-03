from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FileUploadParser
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
    parser_classes = [MultiPartParser, FileUploadParser]
    filter_backends = (SearchFilter,)
    serializer_class = ProductAllCategorySerializer

    @swagger_auto_schema(methods=["get"],
                         responses={200: CategoryAllSerializer, 400: "Bad Request", 404: "Not Found"})
    @action(methods=['get'], detail=False)
    def category_all(self, request, *args, **kwargs):
        company_id = request.user.company_id
        category = Category.objects.filter(company_id=company_id)
        page = self.paginate_queryset(category)
        serializer = CategoryAllSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(methods=["get"], manual_parameters=[openapi.Parameter(
        "id",
        in_=openapi.IN_PATH,
        description="Category ID",
        type=openapi.TYPE_INTEGER
    )], responses={200: CategoryGetOneSerializer, 400: "Bad Request", 404: "Not Found"})
    @action(methods=['get'], detail=True)
    def category_one(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        serializer = CategoryGetOneSerializer(category)
        return Response(serializer.data)

    @swagger_auto_schema(method="get", manual_parameters=[openapi.Parameter(
        "id",
        in_=openapi.IN_PATH,
        description="Product ID",
        type=openapi.TYPE_INTEGER
    )], responses={200: ProductOneSerializer, 400: "Bad Request", 404: "Not Found"})
    @action(methods=['get'], detail=True)
    def product_one(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        serializer = ProductOneSerializer(product)
        return Response(serializer.data)
