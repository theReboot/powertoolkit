from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    pwd1 = forms.CharField(widget=forms.PasswordInput)
    pwd2 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                return email
            else:
                raise forms.ValidationError('Email already in use')

    def clean(self):
        if 'pwd1' in self.cleaned_data and 'pwd2' in self.cleaned_data:
            pwd1 = self.cleaned_data["pwd1"]
            pwd2 = self.cleaned_data["pwd2"]
            if pwd1 != pwd2:
                raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data
