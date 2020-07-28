from django.forms.models import inlineformset_factory
from django import forms
from .models import *

#class ProblemResolutionForm(ModelForm):
#    class Meta:
#        model = ProblemResolution
#        fields = '__all__'

class SearchForm(forms.Form):
    input_text = forms.CharField(label=False,min_length=1, max_length=20, strip=True, widget=forms.TextInput(
        attrs={'placeholder': 'Find problems by name...', 'class': 'form-control mb-2 mr-sm-2'} ))

class ProblemForm(forms.ModelForm):
    error_css_class = 'error'
    class Meta:
        model = Problem
        fields = '__all__'


ProblemResolutionFormSet = inlineformset_factory(Problem, ProblemResolution, form=ProblemForm, fields='__all__' ,extra=1, can_delete=True)
