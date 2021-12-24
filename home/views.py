from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Advertisement, Favourite
from .serializers import (ProfileSerializer, AdvertisementSerializer)
# Create your views here.


class ProfileListView(APIView):
    def get(self, request):
        profile = Profile.objects.get(pk=1)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)


class AdvertisementListView(APIView):
    def get(self, request):
        advertisement = Advertisement.objects.all()
        serializer = AdvertisementSerializer(advertisement, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AdvertisementSerializer(data=request.data,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)


class AdvertisementItemView(APIView):
    def get(self, request, id):
        advertisement = get_object_or_404(Advertisement, pk=id)
        if not advertisement:
            return Response({"error": f"{id} doesn't exist"})
        serializer = AdvertisementSerializer(advertisement)

        return Response(serializer.data)

    def put(self, request, id):
        advertisement = get_object_or_404(Advertisement, pk=id)
        if not advertisement:
            return Response({"error": f"{id} doesn't exist"})
        serializer = AdvertisementSerializer(advertisement)

        return Response(serializer.data)

    def delete(self, request, id):
        advertisement = get_object_or_404(Advertisement, pk=id)
        if not advertisement:
            return Response({"error": f"{id} doesn't exist"})
        serializer = AdvertisementSerializer(advertisement)
        advertisement.delete()

        return Response(serializer.data)


@api_view()
def image(request):
    user = Profile.objects.filter(username='Arpa').first()
    print(user.username, user.id)
    advertisements = Advertisement.objects.select_related('owner').first()
    print(type(advertisements), type(user))
    favourite = Favourite(
        advertisement=advertisements,
        favourite_owner=user
    )
    favourite.save()
    favourite = Favourite.objects.select_related(
        'advertisement', 'favourite_owner')

    print(favourite)
    # for fav in favourite:
    #     print(fav.advertisement.id)
    #     print(fav.favourite_owner.id)

    # for ads in advertisements:
    #     print(ads.id)

    return Response(request, 'home.html', {'user': user})
