from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.office_manager.serializers.product import CategoryGetAllSerializer, CategoryOneProductAll, \
    ProductCreateSerializer, ProductGetAllSerializer, ProductUpdateAllSerializer, GetOneProductSerializer, \
    CreateCategorySerializer
from apps.product.models import Category, Product


class ProductModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Category.objects.all().order_by('-id')
    parser_classes = (MultiPartParser, FileUploadParser)
    filter_backends = (SearchFilter,)

    @swagger_auto_schema(method="get", responses={"200": CategoryGetAllSerializer, "400": "Bad Request"})
    @action(methods=['get'], detail=False)
    def get_all(self, request, *args, **kwargs):
        company = request.user.company_id
        company_all = Category.objects.filter(company=company)
        page = self.paginate_queryset(company_all)
        serializer = CategoryGetAllSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(method='get', manual_parameters=[openapi.Parameter("id", in_=openapi.IN_PATH,
                                                                            description="Category ID",
                                                                            type=openapi.TYPE_STRING)],
                         responses={200: ProductGetAllSerializer, 400: "Bad Request", 404: "Not Found"})
    @action(methods=['get'], detail=True)
    def get_one_category_product(self, request, *args, **kwargs):
        company = Product.objects.filter(category=kwargs['pk'])
        company = company.filter(is_deleted=False)
        page = self.paginate_queryset(company)
        serializer = ProductGetAllSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(methods=['post'], request_body=ProductCreateSerializer,
                         responses={200: "Success Created", 400: "Bad Request"})
    @action(methods=['post'], detail=False)
    def create_product(self, request, *args, **kwargs):
        self.serializer_class = ProductCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully Created"})

    @swagger_auto_schema(method='post', request_body=CreateCategorySerializer,
                         responses={200: "Success Created", 400: "Bad Request"})
    @action(methods=["post"], detail=False)
    def create_category(self, request, *args, **kwargs):
        self.serializer_class = CreateCategorySerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully Created"})

    @swagger_auto_schema(method='get', manual_parameters=[openapi.Parameter("id", in_=openapi.IN_PATH,
                                                                            description="Product ID",
                                                                            type=openapi.TYPE_STRING)])
    @action(methods=['get'], detail=True)
    def get_one_product(self, request, *args, **kwargs):
        self.serializer_class = GetOneProductSerializer
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @swagger_auto_schema(method='put', request_body=ProductUpdateAllSerializer,
                         responses={200: "successfully updated", 400: "Bad Request", 404: "Not Found"})
    @action(methods=['put'], detail=True)
    def update_product(self, request, *args, **kwargs):
        self.serializer_class = ProductUpdateAllSerializer
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "success"})
