from django.db import models

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

    def get_context(self, request):
        context = super().get_context(request)
        learning_sessions = LearningSessionPage.objects.child_of(self).live()
        context['module_sessions'] = learning_sessions
        return context

    content_panels = Page.content_panels + [
        FieldPanel('outline', classname='full'),
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
