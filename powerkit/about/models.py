from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


class AboutPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


@register_snippet
class Metadata(models.Model):
    description = models.CharField(max_length=250)
    keywords = models.TextField(blank=True, null=True)

    panels = [
        FieldPanel('description', classname='full'),
        FieldPanel('keywords', classname='full'),
    ]

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Metadata'
