import django_filters
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import generics, viewsets, renderers
from rest_framework.response import Response
from rest_framework.viewsets import mixins
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from exlib.rest_framework.pagination import PageCodePagination
from .models import User
from .serializers import UserSerializer, UserEasySerializer, AuthenticationSerializer, SendEmailSerializer
from .filters import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageCodePagination
    filter_class = UserFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['post'])
    def send_email(self, request):
        form = SendEmailSerializer(data=request.data)
        if not form.is_valid():
            return Response({'success': False, 'req payload': request.data, 'messages': form.errors}, status=400)
        request.user.send_email(**form.cleaned_data)
        return Response({'success': True})

    @action(detail=False, methods=['post'])
    def info(self, request):
        return Response(UserSerializer(request.user).data)


class LoginView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = AuthenticationSerializer

    def post(self, request, format=None):
        form = AuthenticationSerializer(data=request.data, request=request)
        if form.is_valid():
            auth_login(self.request, form.user)
            return Response({'success': True})
        else:
            return Response({'success': False, 'req payload': request.data, 'messages': form.errors}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def loginout(request):
    auth_logout(request)
    return Response({'success': True})


#****************************************一些示例，复制粘贴用****************************************
# View -> APIView -> GenericAPIView
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from exlib.django.core.serializers.json import DjangoTJSONEncoder


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
        'status': user.status,
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
            'status': user.status,
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
                'status': user.status,
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

