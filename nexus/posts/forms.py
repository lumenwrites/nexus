import itertools

from django.forms import ModelForm
from django import forms
from django.template.defaultfilters import slugify

from .models import Post
from hubs.models import Hub


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'hubs']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'markdown',
                                          'id': 'markdown'}),
            # 'hubs': forms.ModelMultipleChoiceField(queryset=Hub.objects.all(), to_field_name="hubs"),
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

        
