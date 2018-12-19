from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


class SystemPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


@register_snippet
class Agency(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('description', classname='full'),
    ]


@register_snippet
class GencoType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
    ]


@register_snippet
class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
    ]


@register_snippet
class Genco(models.Model):
    name = models.CharField(max_length=200)
    kind = models.ForeignKey(GencoType, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('kind'),
        FieldPanel('capacity'),
        FieldPanel('location'),
    ]


#@register_snippet
#class Disco(models.Model):
#    name = models.CharField(max_length=200)
#
#    def __str__(self):
#        return self.name
#
#    panels = [
#        FieldPanel('name'),
#    ]
