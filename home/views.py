from django.shortcuts import render, get_object_or_404, get_list_or_404
import django_filters.rest_framework

# from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.views import APIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile, Advertisement, Favourite
from .serializers import (
    FavouriteItemSerializer,
    ProfileSerializer,
    AdvertisementSerializer,
    AdvertisementCreateSerializer,
    FavouriteSerializer,
    ImageSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly
from .pagination import DefaultPagination


# Create your views here.


class ProfileListView(APIView):
    def get(self, request):
        profile = Profile.objects.get(pk=1)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)


class AdvertisementListView(generics.ListAPIView):

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_fields = ["title", "rent_fee"]
    search_fields = ["title", "rent_fee"]
    ordering_fields = ["title"]
    pagination_class = DefaultPagination


class AdvertisementCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile_id = get_object_or_404(Profile, user_id=user.id)
        request.data._mutable = True
        if request.data.get("images"):
            images = request.data.pop("images")
            print(images)
        adv_serializer = AdvertisementCreateSerializer(
            data=request.data,
            context={"owner": profile_id},
        )
        adv_serializer.is_valid(raise_exception=True)
        adv_serializer.save()
        if images:
            advertisement = get_object_or_404(Advertisement, pk =adv_serializer.data['id'])
            for img in images:
                data = {"images": img, "advertisement": advertisement.id}
                image_serializer = ImageSerializer(data = data)
                image_serializer.is_valid(raise_exception=True)
                image_serializer.save()
                adv_serializer.data['images'].append(image_serializer.data["images"])
        return Response(adv_serializer.data)


class AdvertisementItemView(APIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get(self, request, id):
        advertisement = get_object_or_404(Advertisement, pk=id)
        serializer = AdvertisementSerializer(advertisement)

        return Response(serializer.data)

    def put(self, request, id):
        advertisement = get_object_or_404(Advertisement, pk=id)
        serializer = AdvertisementSerializer(advertisement)

        return Response(serializer.data)

    def delete(self, request, id):
        advertisement = get_object_or_404(Advertisement, pk=id)
        serializer = AdvertisementSerializer(advertisement)
        advertisement.delete()

        return Response(serializer.data)


class FavouriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = self.request.user
        if user.is_staff:
            favourite = get_list_or_404(Favourite)
            serializer = FavouriteSerializer(favourite, many=True)
            return Response(serializer.data)

        profile_id = get_object_or_404(Profile, user_id=user.id)
        favourite = get_list_or_404(Favourite, favourite_owner=profile_id)
        serializer = FavouriteSerializer(favourite, many=True)

        return Response(serializer.data)


class FavouriteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = self.request.user
        if user.is_staff:
            favourite = get_object_or_404(Favourite, pk=id)
            serializer = FavouriteItemSerializer(favourite)
            return Response(serializer.data)

        profile_id = get_object_or_404(Profile, user_id=user.id)
        favourite = get_object_or_404(Favourite, pk=id, favourite_owner=profile_id)
        serializer = FavouriteItemSerializer(favourite)
        return Response(serializer.data)


@api_view()
def image(request):
    user = Profile.objects.filter(username="Arpa").first()
    print(user.username, user.id)
    advertisements = Advertisement.objects.select_related("owner").first()
    print(type(advertisements), type(user))
    favourite = Favourite(advertisement=advertisements, favourite_owner=user)
    favourite.save()
    favourite = Favourite.objects.select_related("advertisement", "favourite_owner")

    print(favourite)
    # for fav in favourite:
    #     print(fav.advertisement.id)
    #     print(fav.favourite_owner.id)

    # for ads in advertisements:
    #     print(ads.id)

    return Response(request, "home.html", {"user": user})
