from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {'text': 'Текст поста', 'group': 'Группа'}
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'cols': 40, 'rows': 10}
            ),
            'group': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }
