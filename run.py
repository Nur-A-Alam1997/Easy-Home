import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testapp.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# from django.contrib.admin.models import LogEntry

# LogEntry.objects.all().delete()

from football.models import Owner
from football.models import Product


owner = Product.objects.all()
print(Product._meta.fields)

for own in owner:
    print(own.id)
    print(own.title)
    print(own.owner)

from django.db.models import Q
criterion1 = Q(title__contains="Billi")
criterion2 = Q(owner_id=None)
inst = Product.objects.filter(criterion1 & criterion2).first()

# inst.delete()
print(inst)