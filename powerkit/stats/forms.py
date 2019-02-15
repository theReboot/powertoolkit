from django import forms

from stats.models import PerformanceSummary


class PerformanceForm(forms.ModelForm):

    class Meta:
        model = PerformanceSummary
        exclude = []
