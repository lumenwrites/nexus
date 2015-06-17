from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs = {'placeholder': 'E-Mail'})) #reqired=True

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username' : forms.TextInput(attrs = {'placeholder': 'Username'}),
            'email'    : forms.TextInput(attrs = {'placeholder': 'E-Mail'}),
            # These don't work, had to redefine in views(login_or_signup)
            'password1' : forms.PasswordInput(attrs = {'placeholder': 'Password'}),
            'password2' : forms.PasswordInput(attrs = {'placeholder': 'Repeat Password'})
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'website',  'about'] 
        widgets = {
            'username' : forms.TextInput(attrs = {'placeholder': 'Username'}),
            'email'    : forms.TextInput(attrs = {'placeholder': 'E-Mail'}),
            'website'    : forms.TextInput(attrs = {'placeholder': 'Website'}),
            'about'    : forms.Textarea(attrs = {'placeholder': 'About'}),                   
        }
    
