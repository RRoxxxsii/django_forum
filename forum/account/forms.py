from django.contrib.auth.forms import AuthenticationForm
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


class UserEditForm(forms.ModelForm):

    @staticmethod
    def get_tuples_from_genders():
        genders = Gender.objects.all()
        return (gender for gender in genders)

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-lastname'}))

    gender = forms.MultipleChoiceField(label='Gender', required=False)

    profile_information = forms.CharField(widget=forms.Textarea(attrs={'label': 'Profile information',
                                                                       'class': 'form-control',
                                                                       'id': 'exampleFormControlTextarea1',
                                                                       'rows': '3',
                                                                       'placeholder': 'Tell about yourself'}))

    mobile = forms.CharField(label='Mobile', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your mobile', 'id': 'form-lastname'}), required=False)

    telegram = forms.URLField(label='Telegram', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter a link to your telegram if any',
                   'id': 'form-lastname'}), required=False)

    image = forms.ImageField(required=False)

    class Meta:
        model = Author
        fields = ('email', 'user_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True


