"""todoproject URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from todoapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^todo$', views.generalToDo, name='general_todo'),
    url(r'^todo/(?P<todo_id>[0-9]+)$', views.todoById, name='todos_by_id'),
    url(r'^user$', views.user_management, name='user_management'),
    url(r'^user/login$', TokenObtainPairView.as_view(), name='token_obtain'),
    url(r'^user/login/refresh$', TokenRefreshView.as_view(), name='token_obtain_refresh'),
]
