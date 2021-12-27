from django.shortcuts import render, get_object_or_404, get_list_or_404

# from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.views import APIView
from .models import Profile, Advertisement, Favourite
from .serializers import (
    FavouriteItemSerializer,
    ProfileSerializer,
    AdvertisementSerializer,
    FavouriteSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly

# from .shortcuts import get_object_as_list_or_404
# Create your views here.


class ProfileListView(APIView):
    def get(self, request):
        profile = Profile.objects.get(pk=1)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)


class AdvertisementListView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        advertisement = Advertisement.objects.all()
        serializer = AdvertisementSerializer(advertisement, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AdvertisementSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class AdvertisementItemView(APIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]

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


class FavouriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.is_staff:
            favourite = get_list_or_404(
                Favourite,
            )
            serializer = FavouriteSerializer(favourite, many=True)
            return Response(serializer.data)

        user = self.request.user
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
        serializer = FavouriteItemSerializer(
            favourite,
        )
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
