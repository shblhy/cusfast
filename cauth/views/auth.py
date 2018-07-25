from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework import generics, renderers, mixins
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from cauth.models import User
from cauth.serializers import UserSerializer, AuthenticationSerializer, SendEmailSerializer


class AuthView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class LoginView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = AuthenticationSerializer

    def post(self, request, format=None):
        form = self.get_serializer(data=request.data, request=request)
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


class SendEmailView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = SendEmailSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        form = self.get_serializer(data=request.data, request=request)
        if not form.is_valid():
            return Response({'success': False, 'req payload': request.data, 'messages': form.errors}, status=400)
        request.user.send_email(**form.cleaned_data)
        return Response({'success': True})
