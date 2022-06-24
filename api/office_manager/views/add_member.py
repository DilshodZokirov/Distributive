from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.office_manager.serializers.add_member import UserCreateSerializer
from apps.user.models import User


class AddUserModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        pass
