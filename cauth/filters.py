from .models import User
from django_filters.rest_framework import FilterSet
from exlib.django_filters.filterset import NatualFilterSet


class UserFilter(NatualFilterSet):
# class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            'is_superuser': ['exact'],
            'is_staff': ['exact'],
            'username': ['icontains'],
            'nickname': ['icontains'],
            'groups': ['exact']
        }