"""blogapp URL Configuration

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
from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('index', views.index, name='index'),
    path('userdetail', views.userdetail, name='userdetail'),
    path('verify/<auth_token>', views.verify, name='verify'),
   
    path('login1', views.login1, name='login1'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile ,name='profile'),
    path('uprofile', views.uprofile, name='uprofile'),
    path('userdetail', views.userdetail, name='userdetail'),
    path('forgot', views.forgot, name='forgot'),
    path('fpassword', views.fpassword, name='fpassword'),
    path('forpassword', views.forpassword, name='forpassword'),
    path('pass1', views.pass1, name='pass1'),
    path('error', views.error, name='error'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
   
]