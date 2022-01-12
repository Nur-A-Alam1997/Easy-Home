from django_filters.rest_framework import FilterSet
from .models import Advertisement

class AdvertisementFilter(FilterSet):
    class Meta:
        model = Advertisement
        fields={
            'title':['exact'],
            'cost':['lt','gt'],
            'status':['exact']
        }