from django.forms import ModelForm
from django import forms

from .models import Comment

class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = ['body', 'comment_type', 'rating',] # 'comment_type',
        widgets = {
            'rating' : forms.Select(attrs={'id':'rating'})
        }
