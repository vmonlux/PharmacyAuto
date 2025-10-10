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
from django.urls import path, include
from . import views
from auto.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name="home"),
    
    path('backup/', views.backup, name="backup"),
    
    path('omni/', OmniList.as_view(), name='omni-list'),
    path('omni/view/<int:pk>', OmniView.as_view(), name='omni-view'),
    path('omni/update/<int:pk>', OmniUpdate.as_view(), name='omni-update'),
    
    path('aux/', AuxList.as_view(), name='aux-list'),
    path('aux/view/<int:pk>', AuxView.as_view(), name='aux-view'),
    path('aux/update/<int:pk>', AuxUpdate.as_view(), name='aux-update'),
    
    path('ref/', RefList.as_view(), name='ref-list'),
    path('ref/view/<int:pk>', RefView.as_view(), name='ref-view'),
    path('ref/update/<int:pk>', RefUpdate.as_view(), name='ref-update'),
    
    path('lockbox/', BoxList.as_view(), name='box-list'),
    path('lockbox/view/<int:pk>', BoxView.as_view(), name='box-view'),
    path('lockbox/update/<int:pk>', BoxUpdate.as_view(), name='box-update'),

    path('master/omnicell', OmniMaster.as_view(), name='omnimaster'),
    path('master/refrigerator', FlexMaster.as_view(), name='flexmaster'),
    path('master/lockbox', LockMaster.as_view(), name='lockmaster'),
    path('master/aux', AuxMaster.as_view(), name='auxmaster'),

    path('test/', TestView.as_view(), name='test'),
]

