from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name = "homepage"),
    path('desease/<str:pk>', views.desease, name = "desease"),
    path('search/', views.search, name = "search"),
]
