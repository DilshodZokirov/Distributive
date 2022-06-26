from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.office_manager.serializers.worker import UserCreateSerializer, WorkerUserAllSerializer, UserMoveSerializer, \
    UserSalarySerializer
from apps.user.models import User


class WorkerModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = User.objects.all()
    serializer_class = WorkerUserAllSerializer
    filter_backends = (SearchFilter,)

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully Created"})

    @action(methods=['get'], detail=False)
    def worker_list(self, request, *args, **kwargs):
        self.serializer_class = WorkerUserAllSerializer
        company = request.user.company_id
        self.queryset = User.objects.filter(company=company)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def move_agent(self, request, *args, **kwargs):
        self.serializer_class = UserMoveSerializer
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def user_salary(self, request, *args, **kwargs):
        self.serializer_class = UserSalarySerializer
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
    # @action(methods=['get'],detail=)