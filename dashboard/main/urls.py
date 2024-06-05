"""
URL configuration for dashboard project.

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
from django.urls import path,include, re_path
from rest_framework.routers import DefaultRouter
from .views import LoginUser,index,form_handler,DataAPIView,SettingsAPIView,DrawingTypeViewSet,TypesCountViewSet

#router = DefaultRouter()
#router.register(r'groupuser',SettingsAPIView,basename='settings')

urlpatterns = [
    path('index', index, name='index'),
    path('', LoginUser.as_view(), name='log'),
    path('form-handler/', form_handler, name='form_handler'),
    path('api/sensor/sensorlist',DataAPIView.as_view()),
    path('api/groupuser/',SettingsAPIView.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/typescountlist/',TypesCountViewSet.as_view(), name='types_count'),
    path('api/drawingtypelist/',DrawingTypeViewSet.as_view(), name='drawing_type'),
    re_path('^auth/', include('djoser.urls.authtoken')),
]
