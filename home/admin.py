from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile, Advertisement, Images, Favourite

# Register your models here.
User = get_user_model()
# admin.site.register(Profile)
# admin.site.register(Advertisement)


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    pass


class ImagesAdmin(admin.StackedInline):
    model = Images

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 2
        return max_num


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = User
    list_display = ["user", "address"]
    list_filter = ["user", "address"]
    search_fields = [
        "user",
    ]
    list_per_page = 10


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "title",
        "location",
        "area",
        "owner",
        "beds",
        "baths",
        "garages",
        "house_type",
        "cost",
        "image",
        "status",
        "slug",
    ]
    list_filter = ["owner"]
    search_fields = ["title", "cost", "owner__user__username"]
    list_per_page = 10
    inlines = [ImagesAdmin]

    class Meta:
        model = Advertisement


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    pass
