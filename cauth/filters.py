from .models import User
from django_filters.rest_framework import FilterSet


class UserFilter(FilterSet):

    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            'username': ['icontains'],
            'nickname': ['icontains'],
            'status': ['exact'],
            'groups': ['exact']
        }