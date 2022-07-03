"""Distributive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

from Distributive import settings

schema_view = get_swagger_view(title='Pastebin API')

API_TITLE = 'Distributive'
API_DESCRIPTION = 'Agent Manager'
yasg_schema_view = get_schema_view(
    openapi.Info(
        title="Distributive API",
        default_version='version1.0',
        description="Distributive API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dilshodzokirov03@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    # renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
schema_view = get_swagger_view(title=API_TITLE)
urlpatterns = [
    path('swagger/', yasg_schema_view.with_ui('swagger',
                                              cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', yasg_schema_view.with_ui('redoc',
                                            cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('version1/user/', include('api.user.urls')),
    path('version1/office_manager/', include('api.office_manager.urls')),
    path('version1/agent/', include('api.agent.urls')),
    path('version1/delivery/', include('api.delivery.urls')),
    path('version1/manager/', include('api.manager.urls')),
    path("version1/company/", include('api.company.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
