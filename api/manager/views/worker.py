from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.agent.serializers.worker import UserProfileSerializer
from api.manager.serializers.worker import ManagerUserProfileSerializer, UserUpdateProfile
from apps.user.models import User


class ManagerWorkerModelApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = User.objects.all().order_by('-id')
    # serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    filter_backends = (SearchFilter,)

    @swagger_auto_schema(method="get",
                         responses={200: ManagerUserProfileSerializer,
                                    400: "Bad Request",
                                    404: "Not Found"})
    @action(methods=['get'], detail=False)
    def profile_agent(self, request, *args, **kwargs):
        user = request.user.id
        queryset = User.objects.get(pk=user)
        serializer = ManagerUserProfileSerializer(queryset)
        return Response(serializer.data)

    @swagger_auto_schema(methods=['put'], request_body=UserUpdateProfile,
                         responses={200: "Success", 400: "Bad Request"})
    @action(methods=['put'], detail=False)
    def profile_update(self, request):
        self.serializer_class = UserUpdateProfile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully Updated"})
