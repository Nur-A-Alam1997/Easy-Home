from django_filters.rest_framework import FilterSet
from .models import Advertisement

class AdvertisementFilter(FilterSet):
    class Meta:
        model = Advertisement
        fields={
            'title':['exact'],
            'rent_fee':['lt','gt'],
            'status':['exact']
        }