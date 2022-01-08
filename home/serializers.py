from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Advertisement, Favourite, Images

User = get_user_model()
# album = AlbumSerializer(many=False, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.IntegerField(read_only= True)
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["id", "mobile", "address", "created_at", "user"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["id", "images","advertisement"]


class AdvertisementSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many = True,required=False, )
    owner = ProfileSerializer(read_only=True)
    class Meta:
        model = Advertisement
        fields = [
            "id",
            "owner",
            "title",
            "house_type",
            "house_address",
            "rent_fee",
            "image",
            "images",
            "status",
        ]

    # def validate(self, data):
    #     owner = self.context["owner"]
    #     data["owner"] = owner
    #     return data


class AdvertisementCreateSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many=True, required=False, 
                                                read_only=True)
    depth =1
    class Meta:
        model = Advertisement
        read_only_fields = ["id", "owner"]
        fields = [
            "id",
            "owner",
            "title",
            "house_type",
            "house_address",
            "rent_fee",
            "image",
            "images",
        ]



    def validate(self, data):
        owner = self.context["owner"]
        data["owner"] = owner
        return data


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ["id", "favourite_owner", "advertisement"]


class FavouriteItemSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()
    favourite_owner = ProfileSerializer()

    class Meta:
        model = Favourite
        fields = ["id", "favourite_owner", "advertisement"]

class FavouriteItemCreateSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer
    favourite_owner = ProfileSerializer

    class Meta:
        model = Favourite
        fields = ["id", "favourite_owner", "advertisement"]
