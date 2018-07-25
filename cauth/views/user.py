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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    # just demo
    @action(detail=False, methods=['post'])
    def send_email(self, request):
        form = SendEmailSerializer(data=request.data)
        if not form.is_valid():
            return Response({'success': False, 'req payload': request.data, 'messages': form.errors}, status=400)
        request.user.send_email(**form.cleaned_data)
        return Response({'success': True})

