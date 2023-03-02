
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account import views

urlpatterns = [
     path('register/', views.RegisterApi.as_view()),
     path('login/', views.Login.as_view()),
]