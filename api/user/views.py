from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.user.serializers import LoginUserSerializer, RegistrationSerializer
from apps.user.models import User


# class RegisterUserApiView(APIView):
#     def post(self, request):
#         serializer = RegistrationSerializer(data=request.data)
#         data: dict = {}
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             data['message'] = "Success"
#         else:
#             data = serializer.errors
#         return Response(data)


class LoginUserModelView(ModelViewSet):
    parser_classes = [MultiPartParser, ]
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()

    @swagger_auto_schema(method='post', request_body=LoginUserSerializer)
    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = LoginUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        role = user.role
        return Response({
            'user_id': user.pk,
            'token': token.key,
            'role_id': role if role else None
        })

    @swagger_auto_schema(method='post', request_body=RegistrationSerializer)
    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data: dict = {}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data['message'] = "Success"
        else:
            data = serializer.errors
        return Response(data)
