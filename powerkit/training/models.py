from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class ModuleIndex(Page):
    intro = models.TextField(null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        module_pages = ModulePage.objects.child_of(self).live()
        context['modules'] = module_pages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['training.ModulePage']


class ModulePage(Page):
    outline = models.TextField(null=True, blank=True)
    goals = RichTextField(null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        module_sessions = ModuleSessionPage.objects.child_of(self).live()
        context['module_sessions'] = module_sessions
        return context

    content_panels = Page.content_panels + [
        FieldPanel('outline'),
        FieldPanel('goals'),
    ]

    parent_page_types = ['training.ModuleIndex']
    subpage_types = ['training.ModuleSessionPage']


class ModuleSessionPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    parent_page_types = ['training.ModulePage']
