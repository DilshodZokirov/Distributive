from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.office_manager.serializers.product import CategoryGetAllSerializer, CategoryOneProductAll, \
    ProductCreateSerializer, ProductGetAllSerializer, ProductUpdateAllSerializer
from apps.product.models import Category, Product


class ProductModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Category.objects.all().order_by('-id')
    filter_backends = (SearchFilter,)

    @action(methods=['get'], detail=False)
    def get_all(self, request, *args, **kwargs):
        company = request.user.company_id
        company_all = Category.objects.filter(company=company)
        serializer = CategoryGetAllSerializer(company_all, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def get_one_category_product(self, request, *args, **kwargs):
        company = Product.objects.filter(category=kwargs['pk'])
        company = company.filter(is_deleted=False)
        serializer = ProductGetAllSerializer(company, many=True)
        return Response({"products": serializer.data})

    @action(methods=['post'], detail=False)
    def create_product(self, request, *args, **kwargs):
        self.serializer_class = ProductCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully Created Product"})

    @action(methods=['get'], detail=True)
    def get_one_product(self, request, *args, **kwargs):
        pass

    @action(methods=['put'], detail=True)
    def update_product(self, request, *args, **kwargs):
        self.serializer_class = ProductUpdateAllSerializer
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "success"})
