from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    # groups = serializers.StringRelatedField(many=True, read_only=True)
    # groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'telephone', 'is_staff', "is_superuser", 'last_login', 'groups')


class UserEasySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname')


class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(label='用户名')
    password = serializers.CharField(label='密码')
    default_error_messages = {
        'invalid_login': "请输入正确的用户名和密码，注意大小写",
        'inactive': "该账号已被禁用.",
    }
    def __init__(self, **kwargs):
        self.request = kwargs.pop('request', None)
        super(serializers.Serializer, self).__init__(**kwargs)

    @property
    def user(self):
        if hasattr(self, 'user_cache'):
            return self.user_cache

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                self.fail('invalid_login')
            else:
                if not self.user_cache.is_active:
                    self.fail('inactive')
        return attrs


class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(label='标题')
    message = serializers.CharField(label='消息')
    to_email = serializers.CharField(label='收件人')