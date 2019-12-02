from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class Cards(models.Model):
    login = models.CharField(max_length=30)
    number = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=16, null=True, blank=True)
    surname = models.CharField(max_length=16, null=True, blank=True)
    balance = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateField(max_length=16, null=True, blank=True)
    cvv  = models.CharField(max_length=3, blank=True)


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    # python manage.py createsuperuser
    def create_superuser(self, login, is_staff, password):
        user = self.model(
            login=login,
            is_staff=is_staff,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class LoginValue(AbstractBaseUser):
    sys_id = models.AutoField(primary_key=True, blank=True)
    login = models.CharField(max_length=127, unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=11, unique=True, null=False, blank=False, default='')
    iin = models.CharField(max_length=12, unique=True, null=False, blank=False, default='')
    name = models.CharField(max_length=30, null=False, blank=False, default='')
    surname = models.CharField(max_length=30, null=False, blank=False, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "login"
    # REQUIRED_FIELDS must contain all required fields on your User model,
    # but should not contain the USERNAME_FIELD or password as these fields will always be prompted for.
    REQUIRED_FIELDS = ['is_staff', 'iin', 'phone_number', ]

    class Meta:
        app_label = "sign_in"
        db_table = "user_data"

    def __str__(self):
        return self.login

    def get_full_name(self):
        str = self.name + self.surname
        return str

    def get_short_name(self):

        return self.login


def __str__(self):
    return self.iin
# Create your models here.

