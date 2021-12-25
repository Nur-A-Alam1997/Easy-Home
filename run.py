import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyHome.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# from django.contrib.admin.models import LogEntry
from django.db import transaction
# LogEntry.objects.all().delete()
from django.contrib.auth import get_user_model

User = get_user_model()
# from football.models import Owner
# from football.models import Product
from home.models import Profile

with transaction.atomic():
    # owner = Profile.objects.filter(id = 2).first()
    user = User.objects.get(id=1) # admin id
    owner = Profile(
        mobile="0126521",
        address="Dahkds",
        user=user
    )
    # print(Profile._meta.fields)
    owner.save()
    owner.mobile = 364387264
    print(owner.id)
    print(owner.mobile)
    print(owner.user)
    # for own in owner:
    #     print(own.id)
    #     print(own.title)
    #     print(own.owner)

# from django.db.models import Q
# criterion1 = Q(title__contains="Billi")
# criterion2 = Q(owner_id=None)
# inst = Product.objects.filter(criterion1 & criterion2).first()

# inst.delete()
# print(inst)