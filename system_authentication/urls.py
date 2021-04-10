"""system_authentication URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from myapp.views import home, log, reg, reg1, logout, uhome, upload, search, sea, msg, frnd, msgs, req, login, approve, \
    reject, post1, pview, upload1, verify

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('log/', log, name='log'),
    path('reg/', reg, name='reg'),
    path('reg1/', reg1, name='reg1'),
    path('logout/', logout, name='logout'),
    path('uhome/', uhome, name='uhome'),
    path('upload/', upload, name='upload'),
    path('search/', search, name='search'),
    path('sea/', sea, name='sea'),
    path('msg/', msg, name='msg'),
    path('frnd/', frnd, name='frnd'),
    path('msgs/', msgs, name='msgs'),
    path('req/', req, name='req'),
    path('login/', login, name='login'),
    path('approve/', approve, name='approve'),
    path('reject/', reject, name='reject'),
    path('post/', post1, name='post'),
    path('pview/', pview, name='pview'),
    path('upload1/', upload1, name='upload1'),
    path('verify/', verify, name='verify'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
