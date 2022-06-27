from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.user.serializers import LoginUserSerializer, RegistrationSerializer
from apps.user.models import User


class RegisterUserApiView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data: dict = {}
        if serializer.is_valid():
            account: User = serializer.save()
            data['response'] = "Successfully registered new user"
            data['phone_number'] = account.phone_number
        else:
            data = serializer.errors
        return Response(data)


class LoginUserAPIView(APIView):
    def post(self, request):
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
