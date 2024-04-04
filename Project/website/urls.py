"""
URL configuration for Project project.

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
from django.urls import path,include
from website import views

urlpatterns = [
    path('create poll/', views.create_poll, name='create_poll'),
    path('', views.polls_list, name='polls_list'),
    path('vote poll/<int:poll_id>/', views.vote_poll, name='vote_poll'),
    path('poll details/<int:poll_id>/', views.view_poll_votes, name='view_poll_votes'),
    path('my polls/',views.user_polls,name='user_polls'),
    path('poll/update/<int:poll_id>/', views.update_poll, name='update_poll'),
    path('login/',views.custom_login_view,name='login'),
    path('register/',views.custom_register_view,name='register'),
    path('logout/', views.custom_logout_view, name='logout'),
]
