from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from core.forms import RegistrationForm
from training.models import Training, TrainingSchedule, LearningPage


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
            # create training schedule
            _training = Training.objects.create(user=usr)
            # No schedule is marked as current yet (bug or feature?)
            for learning_page in LearningPage.objects.order_by('placement'):
                TrainingSchedule.objects.create(
                    user_training=_training,
                    learning_page=learning_page)

            # authenticate and login
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/learning/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
