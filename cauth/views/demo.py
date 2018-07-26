from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework import generics, viewsets, renderers
from rest_framework.response import Response
from rest_framework.viewsets import mixins
from rest_framework.views import APIView
from exlib.django.core.serializers.json import DjangoTJSONEncoder
from cauth.models import User
from cauth.serializers import UserSerializer


#****************************************一些示例，复制粘贴用****************************************
# View -> APIView -> GenericAPIView


def getuser(request):
    id = request.GET.get('id')
    try:
        id = int(id)
    except Exception as e:
        return HttpResponseBadRequest(e.message)
    user = get_object_or_404(User, pk=id)
    res = {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'email': user.email,
        'telephone': user.telephone,
        'is_staff': user.is_staff,
        'last_login': user.last_login,
        'groups': [g.__unicode__() for g in user.groups.all()]
    }
    return JsonResponse(res)


class DemoUserView(View):
    def get(self, request):
        id = request.GET.get('id')
        try:
            id = int(id)
        except Exception as e:
            return HttpResponseBadRequest(e.message)
        user = get_object_or_404(User, pk=id)
        res = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'email': user.email,
            'telephone': user.telephone,
            'is_staff': user.is_staff,
            'last_login': user.last_login,
            'groups': [g.__unicode__() for g in user.groups.all()]
        }
        return JsonResponse(res)

    def post(self, request):
        return

    def put(self, request):
        return


class DemoUserListView(View):
    def get(self, request):
        users = User.objects.all()
        res = []
        for user in users:
            item = {
                'id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'email': user.email,
                'telephone': user.telephone,
                'is_staff': user.is_staff,
                'last_login': user.last_login,
                'groups': [g.__unicode__() for g in user.groups.all()]
            }
            res.append(item)
        return JsonResponse(res, encoder=DjangoTJSONEncoder, safe=False)


class DemoAPIView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class DemoGListAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, format=None):
        return self.list(request, request, format)


class DemoGRetrieveAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, pk, format=None):
        return self.retrieve(request, request, pk, format)


class DemoListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
