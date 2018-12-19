from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


class StatsPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


@register_snippet
class Disco(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('location'),
    ]

    def __str__(self):
        return self.name


@register_snippet
class MeteringStatus(models.Model):
    disco = models.ForeignKey(Disco, on_delete=models.CASCADE)
    total_customers = models.PositiveIntegerField()
    metered_customers = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    panels = [
        FieldPanel('disco'),
        FieldPanel('total_customers'),
        FieldPanel('metered_customers'),
        FieldPanel('year'),
    ]

    class Meta:
        verbose_name_plural = 'Metering Status'

    def __str__(self):
        return '{} - {}'.format(self.disco, self.year)
