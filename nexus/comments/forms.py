from django.forms import ModelForm
from django import forms

from .models import Comment

class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = ['body', 'rating',] # 'comment_type',
        widgets = {
            'rating' : forms.Select(attrs={'id':'rating'})
        }
