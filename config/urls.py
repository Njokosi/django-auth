"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# Django imports
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

# Rest framework imports
from rest_framework import permissions


# DRF imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# This function attempts to import an admin module in each installed application.
admin.autodiscover()


# Schema view for api documentation
schema_view = get_schema_view(
    openapi.Info(
        title="User API",
        default_version="v1",
        description="A sample API to view users and user authentication",
        terms_of_service="https://www.google.com/policies/terms",
        contact=openapi.Contact(email="njokosi@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
]


urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/documentation/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # path("openapi", get_schema_view(
    #     title="Users API",
    #     description="A sample API for accessing users",
    #     version="0.1.0"), name="openapi-schema"),
]

if not settings.ON_SERVER:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
