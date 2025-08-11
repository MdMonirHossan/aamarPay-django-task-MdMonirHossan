"""
URL configuration for payment_gateway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
)
from libs.utils.swagger.swagger_configurations import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom/project app path
    path('api/user/', include('user.urls')),
    path('api/', include('payment.urls')),
    path('api/', include('activity_log.urls')),
    path('', include('dashboard.urls')),

    # Third party urls (Authentication)
    path('api/auth/token', TokenObtainPairView.as_view(), name='auth_token'),
    path('api/auth/refresh-token', TokenRefreshView.as_view(), name='auth_refresh_token'),

     # Swagger UI urls
    path('swagger<format>', schema_view.without_ui(cache_timeout=0), name='schema_json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema_redoc')
]
