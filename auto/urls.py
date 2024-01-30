"""
URL configuration for auto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views
from auto.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    
    path('omnicell/', OmnicellList.as_view(), name='omnicells'),
    path('omnicell/view/<int:pk>', OmnicellView.as_view(), name='viewOmnicell'),
    path('omnicell/update/<int:pk>', OmnicellUpdate.as_view(), name='updateOmnicell'),
    
    path('aux/', AuxList.as_view(), name='auxs'),
    path('aux/view/<int:pk>', AuxView.as_view(), name='viewAux'),
    path('aux/view/<int:pk>', AuxUpdate.as_view(), name='updateAux'),
    
    path('refrigerator/', RefrigeratorList.as_view(), name='refigerators'),
    path('refrigerator/view/<int:pk>', RefrigeratorView.as_view(), name='viewRefrigerator'),
    path('refrigerator/update/<int:pk>', RefrigeratorUpdate.as_view(), name='updateRefrigerator'),
]
