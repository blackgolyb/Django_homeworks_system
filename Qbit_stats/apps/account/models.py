from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.urls import reverse
from datetime import datetime

class UserManager(BaseUserManager):
    def create_user(self, username, password = None):
        #print(username, password)
        if not username:
                raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have an password")

        user = self.model(
            username = username,
        )

        user.email = self.normalize_email(username+"@qbit.com")
        date_now = datetime.today()
        user.dob = '{}-{}-{}'.format(date_now.year, date_now.month, date_now.day) #"2020-08-12"
        user.url = username
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_teacher(self, username, password):
        user = self.create_user(
            username = username,
            password = password,
        )

        user.is_teacher = True
        user.save(using = self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username = username,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_teacher = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    username            = models.CharField(max_length = 30, unique = True)
    email               = models.EmailField(verbose_name = 'email', max_length = 60, unique = True)
    date_joined         = models.DateTimeField(verbose_name = 'дата вступления', auto_now_add = True)
    last_login          = models.DateTimeField(verbose_name = 'последний вход', auto_now = True)
    is_admin            = models.BooleanField(default = False)
    is_active           = models.BooleanField(default = True)
    is_staff            = models.BooleanField(default = False)
    is_superuser        = models.BooleanField(default = False)
    is_teacher          = models.BooleanField(default = False)
    full_name           = models.CharField(verbose_name = "ФИО", max_length = 60, null = True)
    dob                 = models.DateField(verbose_name = 'дата рождения', blank = True, null = True)
    self_img            = models.ImageField(verbose_name = 'фотография', upload_to = 'profile_image', blank = True)
    url                 = models.SlugField(verbose_name = 'ссылка на профиль', max_length = 130, unique = True)

    USERNAME_FIELD      = 'username'
    REQUIRED_FIELDS     = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def dob_return(self):
        return str(self.dob)

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse('user', kwargs = {"slug": self.url})

    def get_full_name(self):
        return self.full_name

    class Meta:
        verbose_name = u"Пользователь"
        verbose_name_plural = u"Пользователи"


class Groups_of_users(models.Model):
    users    = models.ManyToManyField(User, blank = True, related_name = "groups")
    name     = models.CharField(verbose_name = "название группы", max_length = 30, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Группы"
        verbose_name_plural = u"Группы"
