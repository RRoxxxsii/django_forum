from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def validateEmail(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def create_superuser(self, email, user_name, password, **kwargs):

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **kwargs)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('Необходимо ввести адрес электронной почты'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()

        return user


class Country(models.Model):
    country = models.CharField(max_length=50, verbose_name='Страна')

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('country',)


class Gender(models.Model):
    gender = models.CharField(help_text=_('Гендер'), blank=True, max_length=40, verbose_name='Пол')

    class Meta:
        verbose_name = 'Пол',
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.gender


class Author(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('Почтовый адрес'), unique=True)
    user_name = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    mobile = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name='Внешний ключ гендера')
    profile_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', help_text=_('Фото профиля'), blank=True,
                                      verbose_name='Фото профиля')

    profile_information = models.TextField(help_text='Расскажите о себе', blank=True,
                                           verbose_name='Персональная информация')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Страна')
    telegram_link = models.URLField(blank=True, verbose_name='Телеграмм аккаунт')
    city = models.CharField(max_length=70, blank=True, null=True, verbose_name='Город')

    following = models.ManyToManyField(
        "self", blank=True, related_name="followers", symmetrical=False, verbose_name='Подписки'
    )

    # User Status
    is_active = models.BooleanField(default=False, help_text='Активен ли аккаунт?', verbose_name='Активен')
    is_staff = models.BooleanField(default=False, help_text='Администратор ли сайта?', verbose_name='Администратора')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = _("Аккаунт")
        verbose_name_plural = _("Аккаунты")
        ordering = ('user_name',)

    def __str__(self):
        return self.user_name

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'djangowebforum@gmail.com',
            [self.email],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(Author, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('authors:author_detail_view', kwargs={'pk': self.pk})




