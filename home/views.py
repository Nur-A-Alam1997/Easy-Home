from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Registration, Advertisement
# Create your views here.
def home(request):
    return JsonResponse({"ole":"ole"})


def image(request):
    user = Registration.objects.filter(username__contains='Arpa').first()
    print(user.username,user.id)
    advertisements = Advertisement.objects.filter(id = user.id)
    for ads in advertisements:
        print(ads.title)
    return render(request,'home.html',{'user' : user})