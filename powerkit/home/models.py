from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    #intro = RichTextField(blank=True)
    intro = models.TextField(blank=True)
    top_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    left_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    center_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    right_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('top_image'),
        ImageChooserPanel('left_image'),
        ImageChooserPanel('center_image'),
        ImageChooserPanel('right_image'),
    ]


@register_snippet
class FooterText(models.Model):
    text = models.TextField(blank=True, null=True)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text
