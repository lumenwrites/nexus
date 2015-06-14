from django.forms import ModelForm
from django import forms

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug', 'score','published','number','state', 'posttype']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'class': 'markdown',
                                                 'id': 'markdown'}),            

        }
