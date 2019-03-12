from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel


class AboutPage(Page):
    intro = models.TextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        context['partners'] = Partner.objects.all()
        return context

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


@register_snippet
class Partner(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name', classname='full'),
        ImageChooserPanel('logo'),
    ]
