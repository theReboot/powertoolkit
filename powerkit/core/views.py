from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from core.forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['pwd1']
            usr = User.objects.create_user(
                username=email,
                email=email,
                password=password)
            usr.first_name = first_name
            usr.last_name = last_name
            usr.save()
            messages.info(request, 'You have registered successfully')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
