from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.homepage, name = "homepage"),
    path('desease/<str:pk>', views.desease, name = "desease"),
    path('search/', views.search, name = "search"),
    path('voiceSearch/', views.voice_search, name="search"),
    path('about/', views.about, name="about"),
    path('scrap_desease/<str:pk>', views.desease_scrap, name="desease_scrap"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)