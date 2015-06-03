from django.forms import ModelForm
from django import forms

from .models import Story, Chapter
from hubs.models import Hub
from comments.models import Comment

class StoryForm(ModelForm):
    class Meta:
        model = Story
        exclude = ['author', 'slug', 'score','published',]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'markdown',
                                                 'id': 'markdown'}),            

        }

        # 'hubs': forms.CheckboxSelectMultiple()                    

class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        exclude = ['slug', 'score', 'published', 'story', 'number',]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'})
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body',] 
        
class HubForm(ModelForm):
    hubs = Hub.objects.filter(users_can_create_children=True).order_by('id')
    parent = forms.ModelChoiceField(queryset=hubs)
    parent.empty_label = None
    class Meta:
        model = Hub
        fields = ['parent', 'title'] 
        # widgets = {
        #     'parent' : forms.ChoiceField() #choicesrequired=True, 
        # }
