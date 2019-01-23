from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.utils.html import escape
from django.contrib.auth.decorators import login_required

from training.models import Training, TrainingSchedule, LearningPage,\
    MCQAnswer, UserAnswer, QuestionPage, LearningSessionPage


@login_required
def start_training(request):
    #import pdb;pdb.set_trace()
    try:
        _training = Training.objects.get(user=request.user)
    except Training.DoesNotExist:
        _training = Training.objects.create(user=request.user)
        for learning_page in LearningPage.objects.order_by('placement'):
            TrainingSchedule.objects.create(
                user_training=_training,
                learning_page=learning_page)
    else:
        _training.started = timezone.now()
        _training.save()

    schedules = _training.schedules.order_by('id')
    current = schedules[0]
    current.current = True
    current.save()

    current_page = current.learning_page
    return redirect(current_page.url)


@login_required
def complete(request, id):
    # import pdb;pdb.set_trace()
    _training = Training.objects.get(user=request.user)
    schedules = _training.schedules.all()

    page = LearningPage.objects.get(pk=id)
    complete = schedules.get(learning_page=page)
    complete.completed = True
    complete.current = False
    complete.save()
    #old = schedules.get(current=True)
    #old.completed = True
    #old.current = False
    #old.save()

    pending = schedules.filter(completed=False)
    if not pending:
        _training.completed = timezone.now()
        _training.save()
        #return redirect('/learning/')
        _url = '/learning/'
        return JsonResponse({'redirect_url': _url})
    else:
        if schedules.filter(current=True):
            current = schedules[0]
            current_page = current.learning_page
        else:
            current = pending[0]
            current.current = True
            current.save()
            current_page = current.learning_page
        #return redirect(current_page.url)
        return JsonResponse({'redirect_url': current_page.url})


def continue_training(request):
    _training = Training.objects.get(user=request.user)
    schedules = _training.schedules.all()
    current = schedules.filter(current=True)
    if current:
        current_page = current[0].learning_page
    else:
        current_page = schedules[0].learning_page
    return redirect(current_page.url)


@login_required
def select_answer(request, id):
    #import pdb;pdb.set_trace()
    mcq_answer = get_object_or_404(MCQAnswer, pk=id)
    UserAnswer.objects.create(answer=mcq_answer, user=request.user)
    return JsonResponse(
        {
            'success': True,
            'correct': mcq_answer.correct
        }
    )


@login_required
def get_question(request):
    answered = [
        ans.answer.page.id for ans in UserAnswer.objects.filter(
            user=request.user)
    ]
    questions = QuestionPage.objects.exclude(id__in=answered)
    if not questions:
        answers = UserAnswer.objects.filter(user=request.user)
        correct = len([_ans for _ans in answers if _ans.correct])
        total = answers.count()
        return JsonResponse(
            {
                'lessonCompleted': True,
                'correct': correct,
                'total': total
            }
        )
    qtn = questions[0]
    question = {
        'id': qtn.id,
        'text': qtn.question,
        'title': qtn.title
    }
    answers = [
        {
            'id': ans.id,
            'text': ans.answer,
            'correct': ans.correct
        } for ans in qtn.mcq_answers.all()]
    return JsonResponse(
        {
            'question': question,
            'answers': answers,
            'lessonCompleted': False
        })


def get_sessions(request, id):
    learning_page = get_object_or_404(LearningPage, pk=id)
    _sessions = LearningSessionPage.objects.child_of(learning_page).live()
    out = [
        {
            'id': session.id,
            'title': session.title,
            'text': session.body
        } for session in _sessions]
    return JsonResponse({'sessions': out})
