import itertools

from django.forms import ModelForm
from django import forms
from django.template.defaultfilters import slugify

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'markdown',
                                          'id': 'markdown'}),            
        }



class PromptForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'class': 'markdown',
                                                 'id': 'markdown'}),            

        }

        
