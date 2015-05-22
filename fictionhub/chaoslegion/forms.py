from django.forms import ModelForm
from django import forms

from .models import Post, User

from django.contrib.auth.forms import UserCreationForm

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug', 'score',] 

        

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
        
