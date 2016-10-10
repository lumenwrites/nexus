from django.forms import ModelForm
from django import forms

from .models import Hub


class HubForm(ModelForm):
    hubs = Hub.objects.all().order_by('id')
    # parent = forms.ModelChoiceField(queryset=hubs)
    # parent.empty_label = None
    class Meta:
        model = Hub
        fields = ['title','description'] 
        # widgets = {
        #     'parent' : forms.ChoiceField() #choicesrequired=True, 
        # }
