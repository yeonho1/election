from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError('Must have an email address.')
        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(
            email = email,
            nickname = nickname,
            password = password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=u'이메일'
    )
    nickname = models.CharField(
        max_length=20,
        null=False,
        unique=True,
        verbose_name=u'닉네임'
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nickname

    def __str__(self):
        return self.__unicode__()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']