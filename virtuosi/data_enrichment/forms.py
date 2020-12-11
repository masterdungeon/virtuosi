from django import forms
from django.forms import formset_factory

from .models import Document, Rules, RuleCondition


class DocumentForm(forms.ModelForm):
    document = forms.FileField(widget=forms.FileInput, label='')
    class Meta:
        model = Document
        fields = ('document', )
