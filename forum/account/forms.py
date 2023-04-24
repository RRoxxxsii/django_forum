import re

from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms
from account.models import Author, Gender
from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):
    """
    Login Form with password field and username field
    """

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Введи вашу почту', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(label=_('Введите имя'), min_length=4, max_length=50, help_text=_('Обязательно'))
    email = forms.EmailField(max_length=100, help_text=_('Обязательно'),
                             error_messages={'required': _('Вы должны ввести имя')})

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Имя'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Почта', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Подтверждение пароля'})

    class Meta:
        model = Author
        fields = ('user_name', 'email',)

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        r = Author.objects.filter(user_name__iexact=user_name)
        if r.count():
            raise forms.ValidationError(_('Имя пользователя уже существует'))
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_('Пароли не совпадают'))
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Author.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Пожалуйста, используйте другой адрес почты, этот занят'))
        return email


class UserEditForm(forms.ModelForm):

    @staticmethod
    def get_tuples_from_genders():
        genders = Gender.objects.all()
        return (gender for gender in genders)

    user_name = forms.CharField(
        label='Имя', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Введите ваше имя', 'id': 'form-lastname'}),
        required=True)

    gender = forms.MultipleChoiceField(choices=get_tuples_from_genders(), label='Пол', required=False)

    profile_information = forms.CharField(required=False,
                                          widget=forms.Textarea(attrs={'label': 'Информация о вас',
                                                                       'class': 'form-control',
                                                                       'id': 'exampleFormControlTextarea1',
                                                                       'rows': '3',
                                                                       'placeholder': 'Расскажите о себе'}))

    mobile = forms.CharField(label='Мобильный телефон', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Введите ваш номер', 'id': 'form-lastname'}), required=False)

    telegram = forms.URLField(error_messages={'invalid': 'Кажись, ссылка не действительна'}, label='Телеграм',
                              min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Введите ссылку на ваш телеграм аккаунт',
                   'id': 'form-lastname'}), required=False)

    image = forms.ImageField(required=False)

    class Meta:
        model = Author
        fields = ('user_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True


class UserRestoreForm(forms.ModelForm):
    email = forms.CharField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Введите почту', 'id': 'form-email'}))

    user_name = forms.CharField(
        label='Имя', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Введите ваше имя', 'id': 'form-lastname'}),
        required=True)

    class Meta:
        model = Author
        fields = ['email', 'user_name']


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Почта', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Author.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Похоже, такого email адреса не существует')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Новый пароль', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Введите новый пароль', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Новый пароль', 'id': 'form-new-pass2'}))

