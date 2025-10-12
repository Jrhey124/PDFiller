from django.urls import path
from . import views

urlpatterns = [
    path('generate-preview/', views.generate_and_preview, name='generate_preview'),
]