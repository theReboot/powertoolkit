from django import forms
from tinymce.widgets import TinyMCE


class AssignmentForm(forms.Form):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
