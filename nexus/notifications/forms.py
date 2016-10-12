from django.forms import ModelForm
from django import forms

# from .models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body'] 


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['title'] 
        
