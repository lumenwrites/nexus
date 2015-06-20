from django.forms import ModelForm
from django import forms
from django.template.defaultfilters import slugify

from .models import Post

class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.parentslug = kwargs.pop('parentslug', None)
        super(PostForm, self).__init__(*args, **kwargs)    
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        title = cleaned_data.get("title")

        try:
            post = Post.objects.filter(slug=slugify(title), post_type="story").exists()
        except:
            post = False

        try:
            parent = Post.objects.get(slug=self.parentslug)
            chapter = Post.objects.filter(parent=parent, slug=slugify(title)).exists()            
        except:
            chapter = False

        if post:
            raise forms.ValidationError("A story with this title already exists!")
        elif chapter:
            raise forms.ValidationError("A chapter with this title already exists!")            
        else:
            return self.cleaned_data

    class Meta:
        model = Post
        exclude = ['author', 'slug', 'score','published',
                   'number','state', 'posttype', 'reddit_url', 'views']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'class': 'markdown',
                                                 'id': 'markdown'}),            

        }

