from django.contrib import admin
from .models import Profile, Advertisement, Images, Favourite
# Register your models here.

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
    pass


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    inlines = [ImagesAdmin]

    class Meta:
        model = Advertisement


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    pass
