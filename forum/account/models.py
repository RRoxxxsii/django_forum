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
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('country',)


class Gender(models.Model):
    gender = models.CharField(help_text=_('Гендер'), blank=True, max_length=40)

    class Meta:
        verbose_name = 'Пол',
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.gender


class Author(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('почтовый адрес'), unique=True)
    user_name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', help_text=_('Фото профиля'), blank=True)

    profile_information = models.TextField(help_text='Расскажите о себе', blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    telegram_link = models.URLField(_('Телеграмм аккаунт'), blank=True)
    city = models.CharField(_('Где живете'), max_length=70, blank=True, null=True)

    following = models.ManyToManyField(
        "self", blank=True, related_name="followers", symmetrical=False
    )

    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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




