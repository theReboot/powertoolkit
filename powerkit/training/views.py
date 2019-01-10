from django.shortcuts import redirect
from django.utils import timezone

from training.models import Training


def start_training(request):
    #import pdb;pdb.set_trace()
    _training = Training.objects.get(user=request.user)
    _training.started = timezone.now()
    _training.save()

    schedules = _training.schedules.all()
    current = schedules[0]
    current.current = True
    current.save()

    current_page = current.learning_page
    return redirect(current_page.url)


def complete(request):
    _training = Training.objects.get(user=request.user)
    schedules = _training.schedules.all()
    old = schedules.get(current=True)
    old.completed = True
    old.current = False
    old.save()

    pending = schedules.filter(completed=False)
    if not pending:
        _training.completed = timezone.now()
        _training.save()
        return redirect('/learning/')
    else:
        current = pending[0]
        current.current = True
        current.save()
        current_page = current.learning_page
        return redirect(current_page.url)


def continue_training(request):
    _training = Training.objects.get(user=request.user)
    schedules = _training.schedules.all()
    current = schedules.filter(current=True)
    if current:
        current_page = current[0].learning_page
    else:
        current_page = schedules[0].learning_page
    return redirect(current_page.url)
