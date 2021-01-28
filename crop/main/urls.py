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
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)