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
        
        try:
            # if story with this title already exists
            story_exists = Post.objects.filter(slug=slug, post_type="story").exists()
        except:
            story_exists = False

        try:
            # get story with a slug I've passed
            parent = Post.objects.get(slug=self.storyslug)
            # if chapter with this title already exists in this story
            chapter_exists = Post.objects.filter(parent=parent, slug=slug).exists() 
        except:
            chapter_exists = False

        try:
            # but if I haven't changed the title it's fine
            if self.instance.slug == slug:
                chapter_exists = False
                story_exists = False
        except:
            pass

        if story_exists:
            raise forms.ValidationError("A story with this title already exists!")
        elif chapter_exists:
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

