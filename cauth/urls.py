from django.conf.urls import url, include
from rest_framework import routers
from cauth.views import UserViewSet, GroupViewSet, AuthView, LoginView, loginout, SendEmailView
from cauth.views import DemoUserView, DemoUserListView, DemoAPIView, DemoGListAPIView, DemoGRetrieveAPIView, DemoListAPIView, getuser
router = routers.DefaultRouter(trailing_slash=False)
router.register('user', UserViewSet)
router.register('auth', AuthView)
router.register('group', GroupViewSet)


urlpatterns = [
    url('loginout$', loginout),
    url('login$', LoginView.as_view(), name='login'),
    # url('auth', AuthView.as_view(), name='auth'),
    url('send_email', SendEmailView.as_view(), name='login'),

    # --------------------demo---------------------------
    url('getuser/', getuser),
    url('demouserlist/', DemoUserListView.as_view(), name='courses'),
    url('demouser/', DemoUserView.as_view()),
    url('demouserapiview/', DemoAPIView.as_view()),
    url('demousergrapi/(?P<pk>[0-9]+)/', DemoGRetrieveAPIView.as_view()),
    url('demouserglapi/', DemoGListAPIView.as_view()),
    url('demouserlapi/', DemoListAPIView.as_view()),
    # --------------------demo---------------------------
    url('', include(router.urls)),
]
