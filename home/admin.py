from django.contrib import admin
from .models import Registration, Advertisement, Images
# Register your models here.

# admin.site.register(Registration)
# admin.site.register(Advertisement)


class ImagesAdmin(admin.StackedInline):
    model = Images

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 2
        return max_num

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    pass


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    inlines = [ImagesAdmin]

    class Meta:
       model = Advertisement

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    pass