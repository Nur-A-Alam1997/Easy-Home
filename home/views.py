from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Profile, Advertisement, Favourite
# Create your views here.

def home(request):
    return JsonResponse({"ole":"ole"})


def image(request):
    user = Profile.objects.filter(username='Arpa').first()
    print(user.username,user.id)
    advertisements = Advertisement.objects.select_related('owner').first()
    print(type(advertisements),type(user))
    favourite =  Favourite(
        advertisement = advertisements,
        favourite_owner = user
    )
    favourite.save()
    favourite = Favourite.objects.select_related('advertisement','favourite_owner')
    
    print(favourite)
    # for fav in favourite:
    #     print(fav.advertisement.id)
    #     print(fav.favourite_owner.id)

    # for ads in advertisements:
    #     print(ads.id)

    return render(request,'home.html',{'user' : user})