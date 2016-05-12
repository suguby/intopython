from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

ROLES = (
    (0, 'Foo'),
    (1, 'Bar'),
)


class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        u = self.create_user(email, password=password)
        u.is_admin = True
        u.save(using=self._db)
        return u


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        max_length=54,
        unique=True,
        help_text=_('Required. 54 characters or fewer. Valid email.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    name = models.CharField(_('name'), max_length=64, blank=True)
    is_subscriber = models.BooleanField('Платный подписчик', default=False)

    USERNAME_FIELD = 'email'

    class Meta(AbstractBaseUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    objects = MyUserManager()

    @property
    def username(self):
        return self.email

    @username.setter
    def username(self, value):
        self.email = value

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    # def get_group_permissions(self, obj=None):
    #     return set()
    #
    # def get_all_permissions(self, obj=None):
    #     return set()
    #
    # def has_perm(self, perm, obj=None):
    #     from src.articles.models import Article
    #     if isinstance(obj, Article) and perm == 'view_subscription_article':
    #         if obj.by_subscription:
    #             return self.is_subscriber
    #         return True
    #     return True
    #
    # def has_perms(self, perm_list, obj=None):
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     if app_label == 'auth':
    #         return True if self.is_admin else False
    #     return True

    # Admin required fields
    @property
    def is_staff(self):
        return self.is_admin
