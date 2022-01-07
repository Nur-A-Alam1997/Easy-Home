from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileListView.as_view(), name='home-home'),
    path('dashboard/', views.DashboardListView.as_view(), name='home-dashboard'),
    path('advertisement/', views.AdvertisementListView.as_view(), name='home-advertisement'),
    path('advertisement/create/', views.AdvertisementCreateView.as_view(), name='home-advertisement-create'),
    path('advertisement/<int:id>/', views.AdvertisementItemView.as_view(), name='home-advertiesement-item'),
    path('favourite/', views.FavouriteListView.as_view(), name='home-favourite'),
    path('favourite/<int:id>/', views.FavouriteItemView.as_view(), name='home-favourite-item'),
    path('favourite/create/', views.FavouriteItemCreate.as_view(), name='home-favourite-item-create'),
    path('payment/', views.payment, name='home-payment'),
]