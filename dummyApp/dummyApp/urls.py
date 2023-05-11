"""
URL configuration for dummyApp project.

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
from api.views import SteelDesignList, SteelDesignDetail, generate_report
from rest_framework import routers
from api.views import generate_report, view_report
from django.urls import path
from api.views import view_dwg


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/steeldesigns/', SteelDesignList.as_view(), name='steeldesign-list'),
    path('api/steeldesigns/<int:pk>/', SteelDesignDetail.as_view(), name='steeldesign-detail'),
    path('api/designs/<int:pk>/report/', generate_report, name='generate_report'),
    #path('api/login/', UserLogin.as_view(), name='login')
    path('api/viewreport/', view_report, name='reportpdf'),
    path('api/view-dwg/', view_dwg, name='view_dwg'),
]
