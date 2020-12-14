from django import forms
from django.forms import formset_factory

from .models import Document, Rules, RuleCondition


class DocumentForm(forms.ModelForm):
    document = forms.FileField(widget=forms.FileInput, label="")

    class Meta:
        model = Document
        fields = ("document",)


class RulesView(forms.ModelForm):

    class Meta:
        model = Rules
        fields = ['rule_name', 'rule_desc']


class RuleConditionForm(forms.ModelForm):
    field=forms.CharField(label="Field")
    value_from=forms.IntegerField(label="Value From")
    value_to=forms.IntegerField(label="Value To")
    tag=forms.CharField(label="Tag")

    class Meta:
        model = RuleCondition
        fields = ["field", "value_from", "value_to", "tag"]
