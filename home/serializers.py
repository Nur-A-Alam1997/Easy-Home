
from .models import (Profile,
                     Advertisement,
                     Favourite)
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
# album = AlbumSerializer(many=False, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', ]


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.IntegerField(read_only= True)
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'mobile', 'address', 'created_at', 'user']


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'owner', 'title', 'house_type',
                  'house_address', 'rent_fee', 'image']

    def validate(self, data):
        if data["rent_fee"] == 20000:
            print(data['rent_fee'])
            raise serializers.ValidationError(
                {"rent_fee": f"{data['rent_fee']} rent-fee not allowed"})
        return data


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['id', 'favourite_owner', 'advertisement']


class FavouriteItemSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()
    favourite_owner = ProfileSerializer()

    class Meta:
        model = Favourite
        fields = ['id', 'favourite_owner', 'advertisement']
