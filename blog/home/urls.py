
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from home.views import BlogView, PublicBlog

urlpatterns = [
     path('blog/', BlogView.as_view()),
     path('',PublicBlog.as_view()),
]