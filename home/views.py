from django.shortcuts import render, get_object_or_404, get_list_or_404

# import django_filters.rest_framework

# from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile, Advertisement, Favourite
from .serializers import (
    ProfileSerializer,
    ProfileCreateSerializer,
    AdvertisementSerializer,
    AdvertisementCreateSerializer,
    ImageSerializer,
    FavouriteSerializer,
    FavouriteItemSerializer,
    FavouriteItemCreateFormSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly
from .pagination import DefaultPagination
from .filter import AdvertisementFilter


# Create your views here.


class ProfileListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileCreateSerializer

    def get(self, request):
        profile = Profile.objects.filter(user_id=request.user.id).first()
        if profile:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        res = {"message": "Profile not found"}
        return Response(res, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        profile = Profile.objects.filter(user_id=request.user.id).first()
        if profile:
            serializer = ProfileCreateSerializer(profile)
            return Response(serializer.data)
        profile = request.data.copy()
        profile["user"] = request.user.id
        serializer = ProfileSerializer(data=profile)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DashboardListView(generics.ListAPIView):

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = (
        Advertisement.objects.prefetch_related("owner__user", "images")
        .all()
        .order_by("id")
    )
    serializer_class = AdvertisementSerializer
    # filterset_fields = ["title", "cost", "status"]
    filterset_class = AdvertisementFilter
    search_fields = [
        "title",
        "cost",
        "house_type",
        "location",
        "owner__user__username",
    ]
    ordering_fields = ["id", "status"]
    pagination_class = DefaultPagination


class AdvertisementCreateView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementCreateSerializer

    def post(self, request):
        user = request.user
        profile_id = get_object_or_404(Profile, user_id=user.id)
        adv_serializer = AdvertisementCreateSerializer(
            data=request.data,
            context={"owner": profile_id},
        )
        adv_serializer.is_valid(raise_exception=True)
        adv_serializer.save()
        request.data._mutable = True
        image_array = request.data.pop("images") if request.data.get("images") else None
        if image_array and len(image_array) < 3:
            advertisement_id = adv_serializer.data["id"]
            for img in image_array:
                data = {"images": img, "advertisement": advertisement_id}
                image_serializer = ImageSerializer(data=data)
                image_serializer.is_valid(raise_exception=True)
                image_serializer.save()
                adv_serializer.data["images"].append(image_serializer.data["images"])
        return Response(adv_serializer.data)


class AdvertisementItemView(APIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = AdvertisementSerializer

    def get(self, request, id):
        advertisement = get_object_or_404(
            Advertisement.objects.select_related("owner__user").prefetch_related(
                "images"
            ),
            pk=id,
        )
        serializer = AdvertisementSerializer(advertisement)
        return Response(serializer.data)

    def put(self, request, id):
        user = self.request.user
        profile = get_object_or_404(Profile, user_id=user.id)
        advertisement = get_object_or_404(Advertisement, pk=id, owner=profile)
        serializer = AdvertisementSerializer(advertisement, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        user = self.request.user
        profile = get_object_or_404(Profile, user_id=user.id)
        advertisement = get_object_or_404(Advertisement, pk=id, owner=profile)
        advertisement.delete()

        return Response(status=status.HTTP_200_OK)


class AdvertisementByVendorListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        advertisement = get_list_or_404(
            Advertisement.objects.select_related(
                "owner__user",
            ).prefetch_related("images"),
            owner=id,
        )

        serializer = AdvertisementSerializer(advertisement, many=True)
        return Response(serializer.data)


class FavouriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = self.request.user
        if user.is_staff:
            favourite = get_list_or_404(Favourite)
            serializer = FavouriteSerializer(favourite, many=True)
            return Response(serializer.data)

        favourite = get_list_or_404(
            Favourite.objects.select_related(), favourite_owner__user=user.id
        )
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

        favourite = get_object_or_404(
            Favourite.objects.select_related(
                "favourite_owner__user",
                "favourite_owner",
                "advertisement",
                "advertisement__owner__user",
            ),
            pk=id,
            favourite_owner__user=user.id,
        )
        serializer = FavouriteItemSerializer(favourite)
        return Response(serializer.data)

    def delete(self, request, id):
        user = self.request.user
        if user.is_staff:
            favourite = get_object_or_404(Favourite, pk=id).delete()
            favourite.delete()
            return Response(status=status.HTTP_200_OK)

        favourite = get_object_or_404(Favourite, pk=id, favourite_owner__user=user.id)
        favourite.delete()
        return Response(status=status.HTTP_200_OK)


class FavouriteItemCreate(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavouriteItemCreateFormSerializer

    def post(self, request):
        user = self.request.user
        adv_id = self.request.data.get("id") or None
        profile = get_object_or_404(Profile, user_id=user.id)
        favourite = (
            Favourite.objects.select_related("advertisement", "favourite_owner__user")
            .filter(advertisement__pk=adv_id, favourite_owner__pk=profile.id)
            .first()
        )
        if favourite:
            serializer = FavouriteItemSerializer(favourite)
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)
        advertisement = get_object_or_404(Advertisement, pk=adv_id)
        favourite = {
            "advertisement": advertisement.id,
            "favourite_owner": profile.id,
        }
        serializer = FavouriteSerializer(data=favourite)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.initial_data, status.HTTP_201_CREATED)


@api_view()
def payment(request):
    return render(request, template_name="home.html")
    # (request, "home.html", {"user": user})
