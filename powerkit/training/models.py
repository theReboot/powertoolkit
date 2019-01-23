from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey


class LearningIndex(Page):
    intro = models.TextField(null=True, blank=True)
    description = RichTextField(blank=True, null=True)
    instructor = models.CharField(max_length=200, blank=True)
    audience = models.TextField(null=True, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request):
        context = super().get_context(request)
        # import pdb;pdb.set_trace()
        #child_pages = self.get_children().live()
        #child_pages = LearningPage.objects.child_of(self).order_by(
        #    'placement').live()
        child_pages = LearningPage.objects.child_of(self).live()
        context['modules'] = child_pages
        context['first_module'] = child_pages[0]
        context['duration'] = sum(pg.specific.duration for pg in child_pages)
        if not request.user.is_authenticated:
            return context

        try:
            context['training'] = Training.objects.get(user=request.user)
        except (Training.DoesNotExist, TypeError):
            pass
        schedules = TrainingSchedule.objects.filter(
            user_training__user=request.user).order_by('id')
        context['schedules'] = schedules
        context['completed'] = schedules.filter(completed=True)
        current_schedule = schedules.filter(current=True)
        if current_schedule:
            context['current_schedule'] = current_schedule[0]
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('instructor'),
        FieldPanel('audience', classname='full'),
        FieldPanel('description', classname='full'),
        ImageChooserPanel('featured_image'),
    ]

    subpage_types = ['training.LearningPage']


class LearningPage(Page):
    outline = models.TextField(null=True, blank=True)
    goals = RichTextField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)
    placement = models.PositiveIntegerField(default=1)
    body = RichTextField(null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        # import pdb;pdb.set_trace()

        # For LearningSession children
        learning_sessions = LearningSessionPage.objects.child_of(self).live()
        if learning_sessions:
            #pagination
            paginator = Paginator(learning_sessions, 1)
            page = request.GET.get('page', 1)
            context['module_sessions'] = paginator.get_page(page)

        # For Question children
        question_sessions = QuestionPage.objects.child_of(self).live()
        if question_sessions:
            paginator = Paginator(question_sessions, 1)
            page = request.GET.get('page', 1)
            questions = paginator.get_page(page)
            context['question_sessions'] = questions
            context['question_id'] = questions[0].pk

        return context

    content_panels = Page.content_panels + [
        FieldPanel('outline', classname='full'),
        FieldPanel('body', classname='full'),
        FieldPanel('duration'),
        FieldPanel('goals'),
        FieldPanel('placement'),
    ]

    parent_page_types = ['training.LearningIndex']
    subpage_types = ['training.LearningSessionPage', 'training.QuestionPage']

    @property
    def has_questions(self):
        if QuestionPage.objects.child_of(self):
            return True
        return False


class LearningSessionPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    parent_page_types = ['training.LearningPage']


class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def percent_completion(self):
        if not self.schedules.all():
            return 0
        _completed = self.schedules.filter(completed=True).count()
        _all = self.schedules.count()
        return _completed * 100 / _all


class TrainingSchedule(models.Model):
    user_training = models.ForeignKey(
        Training, on_delete=models.CASCADE, related_name='schedules')
    learning_page = models.ForeignKey(LearningPage, on_delete=models.CASCADE)
    current = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.learning_page.title

    @property
    def pending(self):
        if not self.completed and not self.current:
            return True
        return False

    @property
    def has_questions(self):
        return self.learning_page.has_questions


class MCQPage(Page):
    outline = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)
    placement = models.PositiveIntegerField(default=1)
    body = RichTextField(null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)

        return context

    content_panels = Page.content_panels + [
        FieldPanel('outline', classname='full'),
        FieldPanel('body', classname='full'),
        FieldPanel('duration'),
        FieldPanel('placement'),
    ]

    parent_page_types = ['training.LearningIndex']


class QuestionPage(Page):
    question = RichTextField(null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        #import pdb;pdb.set_trace()
        context['answers'] = MCQAnswer.objects.child_of(self).live()

        return context

    content_panels = Page.content_panels + [
        FieldPanel('question', classname='full'),
        InlinePanel('mcq_answers', label='Answers'),
    ]


class MCQAnswer(Orderable):
    page = ParentalKey(
        QuestionPage,
        on_delete=models.CASCADE,
        related_name='mcq_answers')
    answer = models.TextField(null=True, blank=True)
    correct = models.BooleanField(default=False)

    panels = [
        FieldPanel('answer'),
        FieldPanel('correct')
    ]


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(MCQAnswer, on_delete=models.CASCADE)
    when = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.answer.answer
