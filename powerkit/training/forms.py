from django import forms
from tinymce.widgets import TinyMCE

from training.models import AssignmentAnswer


class AnswerForm(forms.ModelForm):
    answer = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = AssignmentAnswer
        fields = ['answer']


class AssessmentForm(forms.ModelForm):
    comment = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = AssignmentAnswer
        fields = ['comment']
