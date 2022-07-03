from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.agent.serializers.order import OrderListSerializer, CreateOrderSerializer, OrderProductCreateSerializer, \
    OrderEditSerializer, OrderPositionDetailSerializer, OrderDetailAllProductSerializer
from apps.order.models import Order
from apps.order.models.order import OrderProduct


class AgentModelOrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    parser_classes = [MultiPartParser, FileUploadParser]
    queryset = Order.objects.filter(is_deleted=False).order_by('-id')
    filter_backends = (SearchFilter,)
    serializer_class = OrderListSerializer

    @swagger_auto_schema(method="get", responses={200: OrderListSerializer, 400: "Bad Request"})
    @action(methods=['get'], detail=False)
    def order_list(self, request, *args, **kwargs):
        self.serializer_class = OrderListSerializer
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(method="get", manual_parameters=[openapi.Parameter(
        "id",
        in_=openapi.IN_PATH,
        description="Order ID",
        type=openapi.TYPE_INTEGER
    )])
    @action(methods=['get'], detail=True)
    def order_position(self, request, *args, **kwargs):
        self.serializer_class = OrderPositionDetailSerializer
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @swagger_auto_schema(method="get", manual_parameters=[openapi.Parameter(
        "id",
        in_=openapi.IN_PATH,
        description="Order ID",
        type=openapi.TYPE_INTEGER
    )])
    @action(methods=['get'], detail=True)
    def order_detail_all_product(self, request, *args, **kwargs):
        self.serializer_class = OrderDetailAllProductSerializer

    @swagger_auto_schema(method="post", request_body=CreateOrderSerializer,
                         responses={200: "Successfully Created", 400: "Bad Request"})
    @action(methods=['post'], detail=False)
    def create_order(self, request, *args, **kwargs):
        self.serializer_class = CreateOrderSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(method="post", request_body=OrderProductCreateSerializer,
                         responses={200: "Successfully Created", 400: "Bad Request"})
    @action(methods=["post"], detail=False)
    def create_product_order(self, request, *args, **kwargs):
        self.serializer_class = OrderProductCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({200: "Successfully Created"})

    @swagger_auto_schema(method="put",
                         request_body=OrderEditSerializer,
                         manual_parameters=[
                             openapi.Parameter("id",
                                               in_=openapi.IN_PATH,
                                               description="Order Product ID",
                                               type=openapi.TYPE_INTEGER)],
                         responses={200: "Successfully Updated", 400: "Bad Request", 404: "Not Found"})
    @action(methods=["put"], detail=True)
    def order_edit(self, request, *args, **kwargs):
        self.serializer_class = OrderEditSerializer
        order = OrderProduct.objects.get(pk=kwargs['pk'])
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({200:"Successfully Updated"})
