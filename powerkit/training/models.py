from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


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
        learning_pages = LearningPage.objects.child_of(self).order_by(
            'placement').live()
        context['modules'] = learning_pages
        context['duration'] = sum(pg.duration for pg in learning_pages)
        try:
            context['training'] = Training.objects.get(user=request.user)
        except Training.DoesNotExist:
            pass
        schedules = TrainingSchedule.objects.filter(
            user_training__user=request.user)
        context['schedules'] = schedules
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
        learning_sessions = LearningSessionPage.objects.child_of(self).live()

        #pagination
        paginator = Paginator(learning_sessions, 1)
        page = request.GET.get('page', 1)
        context['module_sessions'] = paginator.get_page(page)

        return context

    content_panels = Page.content_panels + [
        FieldPanel('outline', classname='full'),
        FieldPanel('body', classname='full'),
        FieldPanel('duration'),
        FieldPanel('goals'),
        FieldPanel('placement'),
    ]

    parent_page_types = ['training.LearningIndex']
    subpage_types = ['training.LearningSessionPage']


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
