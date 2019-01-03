from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class LearningIndex(Page):
    intro = models.TextField(null=True, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request):
        context = super().get_context(request)
        learning_pages = LearningPage.objects.child_of(self).live()
        context['modules'] = learning_pages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('featured_image'),
    ]

    subpage_types = ['training.LearningPage']


class LearningPage(Page):
    outline = models.TextField(null=True, blank=True)
    goals = RichTextField(null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        learning_sessions = LearningSessionPage.objects.child_of(self).live()
        context['module_sessions'] = learning_sessions
        return context

    content_panels = Page.content_panels + [
        FieldPanel('outline'),
        FieldPanel('goals'),
    ]

    parent_page_types = ['training.LearningIndex']
    subpage_types = ['training.LearningSessionPage']


class LearningSessionPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    parent_page_types = ['training.LearningPage']
