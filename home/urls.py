from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-home'),
    path('image/', views.image, name='home-image'),
]