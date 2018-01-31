from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

name_regex = RegexValidator(regex=r'^[가-힣a-zA-Z]{2,20}',
                            message='이름은 특수문자를 제외한 2자리 이상 20자리 이하로 작성하여야합니다.')
phone_regex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
                             message="전화번호는 '010-1234-5678'혹은 '01012345678'형태로 입력하여야 합니다.")


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_id, password, **extra_fields):
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, password, **extra_fields)

    def create_superuser(self, user_id, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self._create_user(user_id, password, **extra_fields)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(validators=[name_regex], max_length=20)
    phone_number = models.CharField(validators=[phone_regex], max_length=13)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)



    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = [
        'name', 'phone_number',
    ]

    objects = CustomUserManager()

    def get_full_name(self):
        return self.user_id

    def get_short_name(self):
        return self.user_id

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
