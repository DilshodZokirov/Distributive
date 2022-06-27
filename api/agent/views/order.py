from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.agent.serializers.order import OrderListSerializer, CreateOrderSerializer
from apps.order.models import Order


class ModelOrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Order.objects.all().order_by('-id')
    filter_backends = (SearchFilter,)
    serializer_class = OrderListSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateOrderSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})
