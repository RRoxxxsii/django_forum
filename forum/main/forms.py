from account.models import Author
from main.models import Post, FeedBack
from django import forms
from captcha.fields import CaptchaField


class AddCommentForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3',
               'placeholder': 'Заголовок', 'id': 'form-lastname', 'name': 'parent'}), max_length=255,
        label='Заголовок')

    text = forms.CharField(required=False,
                           widget=forms.Textarea(attrs={
                                                        'class': 'form-control',
                                                        'id': 'exampleFormControlTextarea1',
                                                        'rows': '3',
                                                        'placeholder': 'Оставить комментарий'
                           }), label='Комментарий')

    class Meta:
        model = Post
        fields = ('title', 'text')


class FeedBackForm(forms.ModelForm):
    text = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={
                               'class': 'form-control',
                               'id': 'exampleFormControlTextarea1',
                               'rows': '5',
                               'placeholder': 'Задайте вопрос'
                           }), label='Ваш вопрос или пожелание')

    captcha = CaptchaField(error_messages={'invalid': "Капча введена неверно. Пожалуйста, попробуйте еще раз."})

    class Meta:
        model = FeedBack
        fields = ('text',)



