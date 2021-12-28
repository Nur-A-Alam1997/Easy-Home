from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileListView.as_view(), name='home-home'),
    path('advertisement/', views.AdvertisementListView.as_view(), name='home-advertisement'),
    path('advertisement/create/', views.AdvertisementCreateView.as_view(), name='home-advertisement-create'),
    path('favourite/', views.FavouriteListView.as_view(), name='home-favourite'),
    path('favourite/<int:id>/', views.FavouriteItemView.as_view(), name='home-favourite-item'),
    path('advertisement/<int:id>/', views.AdvertisementItemView.as_view(), name='home-advertiesement-item'),
    path('image/', views.image, name='home-image'),
]