# import os;os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cusfast.settings");import django;django.setup()
from django.test import TestCase
from cauth.models import User


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User(id=1,
             username='admin',
             nickname='admin',
             email= 'qq@qq.com',
             is_staff=True,
             is_superuser=True,
             password='pbkdf2_sha256$36000$gic6cD6CQfgr$QXWqtrAfyCFDjl/B+beGfvS9JzMMMCVUgokVJnKP8D4='
        ).save()

    def test_normal_process(self):
        assert User.objects.all().count() == 1
        print('success')

    def test_send_email(self):
        user = User.objects.all()[0]
        user.send_email('test', 'testmessage', '345471536@qq.com')
        print('send_email success')