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
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from auto.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name="home"),
    
    path('backup/', views.backup, name="backup"),
    
    path('db/account/', UserList.as_view(), name='account-list'),
    path('db/account/create/', UserCreate.as_view(), name='account-create'),
    path('db/account/view/<int:pk>', UserView.as_view(), name='account-view'),
    path('db/account/update/<int:pk>', UserUpdate.as_view(), name='account-update'),
    
    path('db/omni/', OmniList.as_view(), name='omni-list'),
    path('db/omni/create/', OmniCreate.as_view(), name='omni-create'),
    path('db/omni/view/<int:pk>', OmniView.as_view(), name='omni-view'),
    path('db/omni/update/<int:pk>', OmniUpdate.as_view(), name='omni-update'),
    
    path('db/aux/', AuxList.as_view(), name='aux-list'),
    path('db/aux/view/<int:pk>', AuxView.as_view(), name='aux-view'),
    path('db/aux/update/<int:pk>', AuxUpdate.as_view(), name='aux-update'),
    
    path('db/ref/', RefList.as_view(), name='ref-list'),
    path('db/ref/create/', RefCreate.as_view(), name='ref-create'),
    path('db/ref/view/<int:pk>', RefView.as_view(), name='ref-view'),
    path('db/ref/update/<int:pk>', RefUpdate.as_view(), name='ref-update'),
    
    path('db/box/', BoxList.as_view(), name='box-list'),
    path('db/box/create/', BoxCreate.as_view(), name='box-create'),
    path('db/box/view/<int:pk>', BoxView.as_view(), name='box-view'),
    path('db/box/update/<int:pk>', BoxUpdate.as_view(), name='box-update'),

    path('db/master/omnicell', OmniMaster.as_view(), name='omnimaster'),
    path('db/master/refrigerator', FlexMaster.as_view(), name='flexmaster'),
    path('db/master/lockbox', LockMaster.as_view(), name='lockmaster'),
    path('db/master/aux', AuxMaster.as_view(), name='auxmaster'),

    path('test/', TestView.as_view(), name='test'),

    path('dash/', DashView.as_view(), name='dash'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/', include('django.contrib.auth.urls')),
]