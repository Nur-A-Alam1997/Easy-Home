# from rest_framework import filters


# filter_backends = (filters.DjangoFilterBackend,)

# def filter_queryset(self, queryset):
#     for backend in list(self.filter_backends):
#         queryset = backend().filter_queryset(self.request, queryset, self)
#     return queryset

# def get(self, request, *args, **kwargs):
#     base_qs = MyModel.objects.all()
#     filtered_qs = self.filter_queryset(base_qs)
#     serializer = MySerializer(filtered_qs, many=True)
#     return Response(serializer.data)


# import django_filters.rest_framework
# from django.contrib.auth.models import User
# from myapp.serializers import UserSerializer
# from rest_framework import generics

# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
