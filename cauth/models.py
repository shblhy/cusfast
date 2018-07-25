from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, blank=True, unique=True)
    nickname = models.CharField(_('nickname'), max_length=150, default='',
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that nickname already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    telephone = models.IntegerField(_('telephone'), blank=True, null=True)
    STATUS_CHOICES = ((0, 'active'), (1, 'disable'))
    status = models.IntegerField(default=0)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname', 'email']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户列表'

    @property
    def get_short_name(self):
        return self.username

    # ---------------------------demo-----------------------------
    def send_email(self, subject, message, to_email):
        from django.core.mail import send_mail
        send_mail(subject, message, '763294911@qq.com', [to_email], fail_silently=False)
