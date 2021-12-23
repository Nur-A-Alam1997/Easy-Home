import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testapp.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from django.db import transaction

from football.models import Owner
from football.models import Product

# owner = Owner(
#     name = "Nur-A-Alam Patwary",
# )
# owner.save()

with transaction.atomic():
    owner = Owner.objects.filter(
        id = 1,
    ).first()


    product = Product(
        title = "Billi",
        owner = owner
    )

    product.save()