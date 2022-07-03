from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.company.serializers.company import DeleteCompanySerializer, CompanyUpdateSerializer
from apps.user.models import Company


class CompanyModelViewSet(ModelViewSet):
    serializer_class = DeleteCompanySerializer
    queryset = Company.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    parser_classes = (MultiPartParser, FileUploadParser)
    filter_backends = (SearchFilter,)

    @swagger_auto_schema(method='put', manual_parameters=[openapi.Parameter(
        "id",
        in_=openapi.IN_PATH,
        description="Company ID",
        type=openapi.TYPE_INTEGER
    )], responses={200: "Successfully Deleted", 400: "Bad Request", 404: "Not Found"})
    @action(methods=["put"], detail=True)
    def delete_company(self, request, *args, **kwargs):
        self.serializer_class = DeleteCompanySerializer
        self.queryset = Company
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({200: "Successfully Deleted"})

    @swagger_auto_schema(method="put", request_body=CompanyUpdateSerializer,
                         responses={200: "successfully updated", 400: "Bad Request", 404: "Not Found"}
                         )
    @action(methods=["put"], detail=True)
    def update_company(self, request, *args, **kwargs):
        self.serializer_class = CompanyUpdateSerializer
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({200: "successfully updated"})
