from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transcription/', views.transcription_audio, name='transcription_audio'),
]
