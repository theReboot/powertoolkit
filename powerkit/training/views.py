from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from post_office import mail

from training.models import Training, TrainingSchedule, LearningPage,\
    MCQAnswer, UserAnswer, QuestionPage, LearningSessionPage, AssignmentPage,\
    AssignmentAnswer
from training.forms import AnswerForm, AssessmentForm


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
def complete(request, id, async=True):
    #import pdb;pdb.set_trace()
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
        if async:
            return JsonResponse({'redirect_url': _url})
        else:
            return redirect(_url)
    else:
        if pending.filter(current=True):
            current = pending[0]
            current_page = current.learning_page
        else:
            current = pending[0]
            current.current = True
            current.save()
            current_page = current.learning_page
        #return redirect(current_page.url)
        if current_page.has_assignments:
            page_url = reverse('assignment', args=[current_page.id])
        else:
            page_url = current_page.url

        if async:
            return JsonResponse({'redirect_url': page_url})
        else:
            return redirect(page_url)


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

    # check if any user answer exists
    if UserAnswer.objects.filter(answer__page=mcq_answer.page):
        return JsonResponse({'success': False, 'message': 'Duplicate answer'})

    UserAnswer.objects.create(answer=mcq_answer, user=request.user)
    return JsonResponse(
        {
            'success': True,
            'correct': mcq_answer.correct
        }
    )


@login_required
def get_intro(request, id):
    #import pdb;pdb.set_trace()
    learning_page = get_object_or_404(LearningPage, pk=id)
    # any answers completed ?
    questions = QuestionPage.objects.child_of(learning_page)
    user_answers = UserAnswer.objects.filter(
        answer__page__in=questions, user=request.user)
    if user_answers:
        return HttpResponseBadRequest('Started already')
        #return redirect('get_question', id=id)
    else:
        return JsonResponse(
            {
                'id': learning_page.id,
                'title': learning_page.title,
                'body': learning_page.body
            }
        )


@login_required
def get_question(request, id):
    learning_page = get_object_or_404(LearningPage, pk=id)
    all_questions = QuestionPage.objects.child_of(learning_page).live()

    answered = [
        ans.answer.page.id for ans in UserAnswer.objects.filter(
            user=request.user, answer__page__in=all_questions)
    ]
    questions = all_questions.exclude(id__in=answered)
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
        'title': qtn.title,
        'explanation': qtn.explanation
    }
    answers = [
        {
            'id': ans.id,
            'text': ans.answer,
            'correct': ans.correct
        } for ans in qtn.mcq_answers.all()]
    question_count = all_questions.count()
    progress_count = question_count - questions.count() + 1
    return JsonResponse(
        {
            'question': question,
            'answers': answers,
            'lessonCompleted': False,
            'questionCount': question_count,
            'progressCount': progress_count
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


@login_required
def get_assignment(request, id):
    #import pdb;pdb.set_trace()
    learning_page = get_object_or_404(LearningPage, pk=id)
    assignment = AssignmentPage.objects.child_of(learning_page).live()[0]

    answer = AssignmentAnswer.objects.filter(
        user=request.user, assignment=assignment)
    if not answer:
        answer_json = None
    else:
        _answer = answer[0]
        answer_json = {
            'id': _answer.id,
            'text': _answer.answer,
            'completed': _answer.completed,
            'assessed': _answer.assessed,
            'comment': _answer.comment
        }

    return JsonResponse({
        'question': {
            'id': assignment.id,
            'title': assignment.title,
            'text': assignment.question
        },
        'answer': answer_json
    })


@login_required
def assignment(request, id):
    learning_page = get_object_or_404(LearningPage, pk=id)
    _asst = AssignmentPage.objects.child_of(learning_page).live()[0]
    answer, _ = AssignmentAnswer.objects.get_or_create(
        assignment=_asst, user=request.user)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        #import pdb;pdb.set_trace()
        if form.is_valid():
            #answer.answer = form.cleaned_data['text']
            #answer.save()
            form.save()
            if form.data.get('submit'):
                answer.completed = timezone.now()
                answer.save()

                #send mail to examiner
                email = _asst.examiner.email
                mail.send(
                    email,
                    'learning@powersmart.ng',
                    template='examiner_template',
                    #context={'assignment_link': _link}
                )
                return redirect('complete_training_sync', id=id)
    else:
        form = AnswerForm(instance=answer)
        #answer = AssignmentAnswer.objects.get(assignment=assignment)
    return render(
        request,
        'training/assignment.html',
        {
            'assignment': _asst,
            'form': form,
            'answer': answer
        })


@login_required
def assessment(request, id):
    answer = get_object_or_404(AssignmentAnswer, pk=id)
    _asst = answer.assignment
    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('assessment_list')
    else:
        form = AssessmentForm(instance=answer)
    return render(
        request,
        'training/assessment.html',
        {
            'assignment': _asst,
            'form': form,
            'answer': answer
        }
    )


@login_required
def assessments(request):
    _asst = AssignmentAnswer.objects.filter(assignment__examiner=request.user)
    return render(request, 'training/assessments.html', {'assessments': _asst})
