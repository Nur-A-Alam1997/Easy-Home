from rest_framework import serializers
from .models import (Profile,
                     Advertisement)


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only= True)
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
