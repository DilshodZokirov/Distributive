from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datetime import timedelta
from datetime import datetime
from api.office_manager.serializers.order import OfficeManagerOrderListSerializer, OrderDetailSerializer, \
    OrderIncomeAllSerializer, IncomeUpdateSerializer, CreditOrderSerializer, CreditOneOrderSerializer
from apps.order.models import Order
from utils import result


class OrderModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = OfficeManagerOrderListSerializer
    queryset = Order.objects.filter(Q(order_position='Basket') | Q(order_position='Verification'))
    filter_backends = (SearchFilter,)

    def list(self, request, *args, **kwargs):
        return super(OrderModelViewSet, self).list(self, request, *args, **kwargs)

    # order detail
    @action(methods=['get'], detail=True)
    def detail_order(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

    # income get
    @action(methods=['get'], detail=False)
    def income_sum_order(self, request, *args, **kwargs):
        order = Order.objects.filter(
            Q(order_position="Verification") |
            Q(order_position='Delivery') |
            Q(order_position="Finish")).order_by('-created_date')
        serializer = OrderIncomeAllSerializer(order, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def income_price_send(self, request, *args, **kwargs):
        self.serializer_class = IncomeUpdateSerializer
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_order_credits(self, request, *args, **kwargs):
        order = Order.objects.filter(Q(paid_position='not_paid') |
                                     Q(paid_position='orphan_paid') |
                                     Q(order_position="Delivery") |
                                     Q(order_position='Finish'))
        serializer = CreditOrderSerializer(order, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def get_one_credit_order(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        serializer = CreditOneOrderSerializer(order)
        today = datetime.today().date()
        created_date = serializer.data.get("created_date")[:10]
        date = result(today=today, created_date=created_date)
        serializer.data["date"] = date
        return Response(serializer.data)
