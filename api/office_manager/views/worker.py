from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FileUploadParser, MultiPartParser
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
    parser_classes = [FileUploadParser]
    serializer_class = WorkerUserAllSerializer
    filter_backends = (SearchFilter,)

    @swagger_auto_schema(method="post", request_body=UserCreateSerializer,
                         responses={200: "Successfully Created", 400: "Bad Request"})
    @action(methods=["post"], detail=False)
    def create_worker(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully Created"})

    @swagger_auto_schema(method="get", responses={200: WorkerUserAllSerializer, 400: "Bad Request", 404: "Not Found"})
    @action(methods=['get'], detail=False)
    def worker_list(self, request, *args, **kwargs):
        self.serializer_class = WorkerUserAllSerializer
        company = request.user.company_id
        self.queryset = User.objects.filter(company=company)
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(method="get", manual_parameters=[openapi.Parameter("id", in_=openapi.IN_PATH,
                                                                            description="Worker ID",
                                                                            type=openapi.TYPE_INTEGER)],
                         responses={200: UserMoveSerializer, 400: "Bad Request", 404: "Not Found"})
    @action(methods=['get'], detail=True)
    def user_salary(self, request, *args, **kwargs):
        self.serializer_class = UserSalarySerializer
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
