from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.agent.serializers.worker import UserProfileSerializer
from apps.user.models import User


class ManagerWorkerModelApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = User.objects.all().order_by('-id')
    filter_backends = (SearchFilter,)
    serializer_class = UserProfileSerializer

    @action(methods=['get'], detail=False)
    def profile_agent(self, request, *args, **kwargs):
        user = request.user.id
        queryset = User.objects.get(pk=user)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)
