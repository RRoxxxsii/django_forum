from django.contrib.auth.forms import AuthenticationForm
from django import forms
from account.models import Author
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

    user_name = forms.CharField(label=_('Enter your name'), min_length=4, max_length=50, help_text=_('Required'))
    email = forms.EmailField(max_length=100, help_text=_('Required'),
                             error_messages={'required': _('Sorry, you need to write an email.')})

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
        user_name = self.cleaned_data['user_name'].lower()
        r = Author.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError(_('Username already exists.'))
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_('Passwords do not match.'))
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Author.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Please use another email, that is already taken'))
        return email

