from django.forms import ModelForm
from django import forms

from .models import Prompt


class PromptForm(ModelForm):
    class Meta:
        model = Prompt
        fields = ['prompt', 'prompt_type'] 
        # widgets = {
        #     'parent' : forms.ChoiceField() #choicesrequired=True, 
        # }
