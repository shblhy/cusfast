from rest_framework import generics, viewsets, renderers
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from cauth.models import User
from cauth.serializers import UserSerializer, UserEasySerializer, AuthenticationSerializer, SendEmailSerializer
from cauth.filters import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    permission_classes = (IsAuthenticated,)

    # just demo
    @action(detail=False, methods=['post'])
    def send_email(self, request):
        serializer = SendEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'req payload': request.data, 'messages': serializer.errors}, status=400)
        try:
            request.user.send_email(**serializer.data)
            return Response({'msg': "发送邮件成功"})
        except Exception as e:
            return Response({'req payload': request.data, 'msg': "发送邮件失败:%s" % (e,)}, status=400)
