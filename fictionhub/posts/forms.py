import itertools

from django.forms import ModelForm
from django import forms
from django.template.defaultfilters import slugify

from .models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.storyslug = kwargs.pop('storyslug', None)
        super(PostForm, self).__init__(*args, **kwargs)    
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        title = cleaned_data.get("title")
        slug = slugify(title)

        return self.cleaned_data        

    class Meta:
        model = Post
        fields = ['title', 'body', 'hubs']
        # exclude = ['author', 'slug', 'score','published',
        #            'number','state', 'posttype', 'reddit_url', 'views', 'post_type','pub_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
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

        
