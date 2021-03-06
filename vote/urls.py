"""election URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.main, name='votemain'),
    path('view/<int:id>', views.viewvote, name='viewvote'),
    path('vote/<int:id>', views.vote, name='vote'),
    path('close/<int:id>', views.closevote, name='closevote'),
    path('delete/<int:id>', views.deletevote, name='deletevote'),
    path('logout', LogoutView.as_view(next_page='votemain'), name='logout'),
    path('login', views.login_view, name='login'),
    path('create', views.createVote, name='createvote'),
]
