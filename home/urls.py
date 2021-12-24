from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='home-home'),
    path('advertisement/', views.AdvertisementListView.as_view(), name='home-advertisement'),
    path('advertisement/<int:id>/', views.AdvertisementItemView.as_view(), name='home-advertiesement-item'),
    path('image/', views.image, name='home-image'),
]