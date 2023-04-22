from main.models import Post
from django import forms


class AddCommentForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3',
               'placeholder': 'Заголовок', 'id': 'form-lastname'}), max_length=255,
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

