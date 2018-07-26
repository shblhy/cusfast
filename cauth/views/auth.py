from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework import generics, renderers, mixins, viewsets
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cauth.models import User
from cauth.serializers import UserSerializer, AuthenticationSerializer, SendEmailSerializer


class AuthView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class LoginView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = AuthenticationSerializer

    def post(self, request, format=None):
        form = self.get_serializer(data=request.data, request=request)
        if form.is_valid():
            auth_login(self.request, form.user)
            return Response({'data': UserSerializer(request.user).data})
        else:
            return Response({'req payload': request.data, 'msg': form.errors}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def loginout(request):
    auth_logout(request)
    return Response({'msg': "已经登出"})


class SendEmailView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = SendEmailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'req payload': request.data, 'messages': serializer.errors}, status=400)
        try:
            request.user.send_email(**serializer.data)
            return Response({'msg': "发送邮件成功"})
        except Exception as e:
            return Response({'req payload': request.data, 'msg': "发送邮件失败:%s" % (e,)}, status=400)
