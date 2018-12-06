from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class IssuePage(Page):
    intro = models.TextField(blank=True, null=True)
    key_players = models.TextField(blank=True, null=True)
    player_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    policy_background = models.TextField(blank=True, null=True)
    policy_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('key_players', classname='full'),
        ImageChooserPanel('player_image'),
        FieldPanel('policy_background', classname='full'),
        ImageChooserPanel('policy_image'),
        InlinePanel('issue_points', label='Key Questions'),
    ]


@register_snippet
class Point(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(blank=True, null=True)

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    def __str__(self):
        return self.question


class IssuePoint(Orderable, models.Model):
    page = ParentalKey(
        'issue.IssuePage',
        on_delete=models.CASCADE,
        related_name='issue_points'
    )
    point = models.ForeignKey(
        'issue.Point',
        on_delete=models.CASCADE,
        related_name='+'
    )

    class Meta:
        verbose_name = 'Issue point'
        verbose_name_plural = 'Issue points'

    panels = [
        SnippetChooserPanel('point')
    ]
