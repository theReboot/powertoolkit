from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Contact(models.Model):
    intro = models.TextField(blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200, blank=True)

    panels = [
        FieldPanel('intro', classname='full'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('address'),
    ]
